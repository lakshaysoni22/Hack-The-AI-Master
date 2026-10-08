try:
    import docker
except ImportError:
    docker = None
import os
import re
import json

def get_docker_client():
    try:
        return docker.from_env()
    except Exception as e:
        print(f"Error connecting to Docker daemon: {e}")
        return None

def start_lab_container(lab_id, user_id):
    """
    Spins up a Docker container for the given manual lab.
    Returns the container's IP address or None on failure.
    """
    client = get_docker_client()
    if not client:
        return None, "Docker not available on the host."

    # We will let the code below dynamically check if the lab directory exists
    # instead of hardcoding 'mlab2'.
    image_tag = f"hacktheai_{lab_id}"
    container_name = f"ctf_{lab_id}_user_{user_id}"
    network_name = f"ctf_lab_net_{user_id}"

    # Build the image if it doesn't exist
    try:
        client.images.get(image_tag)
    except docker.errors.ImageNotFound:
        lab_dir = os.path.join(os.path.dirname(__file__), '..', 'labs', lab_id)
        if not os.path.exists(lab_dir):
             return None, f"Lab directory {lab_dir} not found."
        try:
            print(f"Building Docker image for {lab_id}...")
            client.images.build(path=lab_dir, tag=image_tag, rm=True)
        except Exception as e:
            return None, f"Failed to build Docker image: {e}"

    # Stop and remove existing container for this user if it exists
    try:
        old_container = client.containers.get(container_name)
        old_container.stop()
        old_container.remove()
    except docker.errors.NotFound:
        pass

    # Ensure isolated network exists
    try:
        network = client.networks.get(network_name)
    except docker.errors.NotFound:
        network = client.networks.create(network_name, driver="bridge", internal=True)

    # Calculate timeouts
    timeout = int(os.environ.get("LAB_CONTAINER_TIMEOUT", 3600))
    import time
    expiry_time = str(int(time.time()) + timeout)

    try:
        container = client.containers.run(
            image_tag,
            name=container_name,
            detach=True,
            network=network_name,
            mem_limit="256m",
            cpu_quota=50000, # 0.5 CPU
            pids_limit=50,
            labels={"ctf_expiry": expiry_time}
        )
        
        # Get the IP address
        container.reload()
        ip_address = container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress']
        return ip_address, "Success"
        
    except Exception as e:
        return None, f"Failed to start container: {e}"

def stop_lab_container(container_id):
    """
    Stops a running lab container.
    """
    client = get_docker_client()
    if not client:
        return False
        
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return True
    except Exception:
        return False


# =========================================================================
# Uploaded Lab Container Management (ZIP-to-Interactive Lab Engine)
# =========================================================================

import time
import logging
import random

logger = logging.getLogger(__name__)

# Track allocated ports to avoid collisions
_allocated_ports = set()


def _find_available_port(port_min=10000, port_max=20000):
    """Find an available port in the given range."""
    import socket
    attempts = 0
    while attempts < 100:
        port = random.randint(port_min, port_max)
        if port in _allocated_ports:
            attempts += 1
            continue
        # Check if port is actually free
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                _allocated_ports.add(port)
                return port
        except OSError:
            attempts += 1
            continue
    return None


def _find_entry_script(build_context, dockerfile_abs=None):
    """Best-effort detection of the lab's Python entry script from its
    Dockerfile's CMD/ENTRYPOINT (the same source of truth Docker itself
    uses). This lets the native fallback find the right file even when the
    Flask app isn't a top-level app.py (e.g. it lives at app/app.py inside a
    package-like subdirectory), instead of assuming a fixed layout.
    """
    candidates = []
    if dockerfile_abs and os.path.isfile(dockerfile_abs):
        candidates.append(dockerfile_abs)
    default_df = os.path.join(build_context, "Dockerfile")
    if default_df not in candidates and os.path.isfile(default_df):
        candidates.append(default_df)

    for df in candidates:
        try:
            content = open(df, "r", errors="ignore").read()
        except OSError:
            continue
        for match in re.finditer(r'^\s*(?:CMD|ENTRYPOINT)\s+(.+)$', content, re.MULTILINE):
            raw = match.group(1).strip()
            try:
                parts = json.loads(raw) if raw.startswith('[') else raw.split()
            except Exception:
                parts = raw.split()
            for part in parts:
                if isinstance(part, str) and part.endswith('.py'):
                    return part

    return "app.py"


def start_uploaded_lab_container(lab_id, session_id, lab_path, docker_config,
                                  port_min=10000, port_max=20000, timeout=3600):
    """
    Spin up a Docker container for an uploaded lab with port mapping.
    
    Args:
        lab_id: The uploaded lab ID.
        session_id: The lab session ID (unique per user+lab).
        lab_path: Absolute path to the extracted lab directory containing Dockerfile.
        docker_config: Dict with dockerfile_path, ports, etc.
        port_min: Minimum port for dynamic allocation.
        port_max: Maximum port for dynamic allocation.
        timeout: Container timeout in seconds.
        
    Returns:
        (host_port, container_id, message) tuple.
    """
    client = get_docker_client()
    
    if not client:
        # NATIVE FALLBACK EXECUTION
        import subprocess
        import sys
        
        if docker_config.get('dockerfile_path'):
            dockerfile_rel = docker_config['dockerfile_path']
            dockerfile_abs = os.path.join(lab_path, dockerfile_rel)
            build_context = os.path.dirname(dockerfile_abs)
        else:
            build_context = lab_path
            
        if not os.path.isdir(build_context):
            return None, None, f"Lab directory not found for native fallback: {build_context}"

        host_port = _find_available_port(port_min, port_max)
        if not host_port:
            return None, None, "Docker is not available and no free ports for native fallback."

        entry_rel = _find_entry_script(
            build_context,
            dockerfile_abs if docker_config.get('dockerfile_path') else None,
        )
        entry_abs = os.path.join(build_context, entry_rel)
        if not os.path.isfile(entry_abs):
            # Fall back to a plain top-level app.py if detection missed.
            entry_abs = os.path.join(build_context, "app.py")

        wrapper = f"""
import sys
import os
import importlib.util

build_context = sys.argv[1]
host_port = int(sys.argv[2])
entry_path = sys.argv[3]

sys.path.insert(0, build_context)
sys.path.insert(0, os.path.dirname(entry_path))
os.chdir(build_context)

# Load the entry script directly by file path (rather than "import app"),
# so this works whether the Flask app lives at a top-level app.py or nested
# inside a package-like subdirectory (e.g. app/app.py). Loading it under a
# distinct module name (not "__main__") means any "if __name__ == '__main__'"
# block in the lab's own code is skipped, since we drive startup ourselves.
spec = importlib.util.spec_from_file_location("lab_app_entry", entry_path)
mod = importlib.util.module_from_spec(spec)
# Register in sys.modules before executing: Flask's own root-path detection
# (used to find the templates/static folders next to app.py) looks the
# module up by name in sys.modules, so this must happen first.
sys.modules["lab_app_entry"] = mod
spec.loader.exec_module(mod)

if not hasattr(mod, 'DB_PATH') or not os.path.exists(mod.DB_PATH):
    try:
        mod.init_db()
    except Exception:
        pass

mod.app.run(host='127.0.0.1', port=host_port, debug=False, use_reloader=False)
"""
        try:
            # Cross-platform: launch the wrapper script directly with the current
            # Python interpreter, redirecting output to a log file. No cmd.exe/.bat
            # dependency, so this works on Linux/macOS as well as Windows.
            log_path = os.path.join(build_context, "native_fallback.log")
            script_path = os.path.join(build_context, "run_native.py")

            with open(script_path, "w") as f:
                f.write(wrapper)

            log_fh = open(log_path, "w")

            popen_kwargs = {
                "cwd": build_context,
                "stdout": log_fh,
                "stderr": subprocess.STDOUT,
            }
            # Strip Werkzeug reloader env vars before launching. When the
            # platform's own dev server runs with debug=True, Werkzeug's
            # auto-reloader sets WERKZEUG_SERVER_FD (and WERKZEUG_RUN_MAIN) in
            # its own process to hand an already-open socket fd across a
            # fork. Those vars are inherited by any subprocess we spawn by
            # default, so the lab's own Werkzeug server then tries to reuse
            # a socket fd that doesn't exist in the new process, crashing
            # with "OSError: [Errno 9] Bad file descriptor". The lab process
            # needs a clean environment so it opens its own fresh socket.
            child_env = os.environ.copy()
            child_env.pop("WERKZEUG_SERVER_FD", None)
            child_env.pop("WERKZEUG_RUN_MAIN", None)
            popen_kwargs["env"] = child_env
            if os.name == "nt":
                popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                popen_kwargs["start_new_session"] = True

            p = subprocess.Popen(
                [sys.executable, script_path, build_context, str(host_port), entry_abs],
                **popen_kwargs,
            )
            logger.info(f"Native fallback started with PID {p.pid} on port {host_port}")

            # Verify the app actually came up before declaring success -
            # otherwise a lab that crashes on import/startup silently reports
            # "Success" and the learner just sees a generic connection error
            # with no way to know what went wrong.
            import socket
            deadline = time.time() + 8
            up = False
            while time.time() < deadline:
                if p.poll() is not None:
                    break  # process already exited
                try:
                    with socket.create_connection(("127.0.0.1", host_port), timeout=0.3):
                        up = True
                        break
                except OSError:
                    time.sleep(0.25)

            if not up:
                _allocated_ports.discard(host_port)
                try:
                    p.terminate()
                except Exception:
                    pass
                log_fh.flush()
                try:
                    with open(log_path, "r", errors="ignore") as lf:
                        tail = lf.read()[-2000:]
                except OSError:
                    tail = "(no log output captured)"
                logger.error(f"Native fallback for {lab_path} failed to bind port {host_port}. Log:\n{tail}")
                return None, None, (
                    "The lab application failed to start. Details from its log:\n" + tail
                )

            return host_port, f"native_pid_{p.pid}", "Success"
        except Exception as e:
            return None, None, f"Docker is not available and native fallback failed: {e}"

    image_tag = f"hacktheai_uploaded_{lab_id}"
    container_name = f"ctf_uploaded_{session_id}"

    # Determine the build context directory
    if docker_config.get('dockerfile_path'):
        dockerfile_rel = docker_config['dockerfile_path']
        # The build context is the directory containing the Dockerfile
        dockerfile_abs = os.path.join(lab_path, dockerfile_rel)
        build_context = os.path.dirname(dockerfile_abs)
        dockerfile_name = os.path.basename(dockerfile_abs)
    else:
        build_context = lab_path
        dockerfile_name = 'Dockerfile'

    # Build the image if it doesn't exist
    try:
        client.images.get(image_tag)
        logger.info(f"Image {image_tag} already exists, reusing.")
    except docker.errors.ImageNotFound:
        if not os.path.isdir(build_context):
            return None, None, f"Lab build directory not found: {build_context}"

        dockerfile_path = os.path.join(build_context, dockerfile_name)
        if not os.path.isfile(dockerfile_path):
            return None, None, f"Dockerfile not found at {dockerfile_path}"

        try:
            logger.info(f"Building Docker image {image_tag} from {build_context}...")
            client.images.build(
                path=build_context,
                dockerfile=dockerfile_name,
                tag=image_tag,
                rm=True,
                forcerm=True,
            )
            logger.info(f"Successfully built image {image_tag}")
        except Exception as e:
            logger.error(f"Failed to build Docker image: {e}")
            return None, None, f"Failed to build target application: {e}"

    # Stop and remove existing container for this session
    try:
        old_container = client.containers.get(container_name)
        old_container.stop(timeout=5)
        old_container.remove(force=True)
    except docker.errors.NotFound:
        pass
    except Exception as e:
        logger.warning(f"Error cleaning up old container: {e}")

    # Find an available port
    container_port = docker_config.get('ports', [5000])[0]
    host_port = _find_available_port(port_min, port_max)
    if not host_port:
        return None, None, "No available ports for the lab container."

    # Calculate expiry
    expiry_time = str(int(time.time()) + timeout)

    try:
        container = client.containers.run(
            image_tag,
            name=container_name,
            detach=True,
            ports={f'{container_port}/tcp': ('127.0.0.1', host_port)},
            mem_limit="256m",
            cpu_quota=50000,      # 0.5 CPU
            pids_limit=50,
            read_only=False,       # Some apps need write access to temp dirs
            labels={
                "ctf_expiry": expiry_time,
                "ctf_session": session_id,
                "ctf_lab": lab_id,
                "ctf_type": "uploaded_lab",
            },
            environment={
                "LAB_SESSION_ID": session_id,
            },
        )

        logger.info(f"Started container {container_name} on port {host_port}")
        return host_port, container.id, "Success"

    except Exception as e:
        # Release the port if container failed to start
        _allocated_ports.discard(host_port)
        logger.error(f"Failed to start container: {e}")
        return None, None, f"Failed to start target environment: {e}"


def stop_uploaded_lab_container(session_id, container_id=None):
    """Stop and remove an uploaded lab container.
    
    Args:
        session_id: Lab session ID.
        container_id: Optional Docker container ID. If not provided, looks up by name.
        
    Returns:
        True if stopped successfully, False otherwise.
    """
    if container_id and container_id.startswith('native_pid_'):
        pid = int(container_id.split('_')[-1])
        try:
            import psutil
            p = psutil.Process(pid)
            p.terminate()
            logger.info(f"Terminated native fallback PID {pid}")
            return True
        except Exception as e:
            logger.warning(f"Failed to terminate native PID {pid}: {e}")
            return False

    client = get_docker_client()
    if not client:
        return False

    container_name = f"ctf_uploaded_{session_id}"

    try:
        if container_id:
            container = client.containers.get(container_id)
        else:
            container = client.containers.get(container_name)

        # Get the port mapping to release
        ports = container.ports
        for bindings in ports.values():
            if bindings:
                for binding in bindings:
                    port = int(binding.get('HostPort', 0))
                    _allocated_ports.discard(port)

        container.stop(timeout=5)
        container.remove(force=True)
        logger.info(f"Stopped and removed container {container_name}")
        return True

    except docker.errors.NotFound:
        logger.warning(f"Container {container_name} not found for cleanup.")
        return True  # Already gone
    except Exception as e:
        logger.error(f"Error stopping container {container_name}: {e}")
        return False


def get_uploaded_lab_container_status(session_id, container_id=None):
    """Check the status of an uploaded lab container.
    
    Returns:
        Dict with status info, or None if not found.
    """
    client = get_docker_client()
    if not client:
        return {'status': 'docker_unavailable'}

    container_name = f"ctf_uploaded_{session_id}"

    try:
        if container_id:
            container = client.containers.get(container_id)
        else:
            container = client.containers.get(container_name)

        container.reload()
        return {
            'status': container.status,  # running, exited, etc.
            'container_id': container.id,
            'name': container.name,
        }
    except docker.errors.NotFound:
        return {'status': 'not_found'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


def is_target_alive(port, timeout=0.5):
    """Quick check for whether anything is actually listening on
    127.0.0.1:port right now. Works for both the Docker path and the
    native-process fallback, since either way the lab's app ends up bound
    to a host port - if nothing answers, the port is dead regardless of
    how it was started.
    """
    import socket
    if not port:
        return False
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def cleanup_expired_containers():
    """Clean up all expired uploaded lab containers.
    
    Returns:
        Number of containers cleaned up.
    """
    client = get_docker_client()
    if not client:
        return 0

    cleaned = 0
    current_time = int(time.time())

    try:
        containers = client.containers.list(
            all=True,
            filters={'label': 'ctf_type=uploaded_lab'}
        )

        for container in containers:
            expiry = container.labels.get('ctf_expiry', '0')
            try:
                expiry_time = int(expiry)
            except ValueError:
                expiry_time = 0

            if current_time > expiry_time:
                session_id = container.labels.get('ctf_session', '')
                try:
                    # Release port
                    ports = container.ports
                    for bindings in ports.values():
                        if bindings:
                            for binding in bindings:
                                port = int(binding.get('HostPort', 0))
                                _allocated_ports.discard(port)

                    container.stop(timeout=5)
                    container.remove(force=True)
                    cleaned += 1
                    logger.info(f"Cleaned up expired container for session {session_id}")
                except Exception as e:
                    logger.error(f"Error cleaning up container: {e}")

    except Exception as e:
        logger.error(f"Error listing containers for cleanup: {e}")

    return cleaned

