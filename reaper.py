import docker
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_docker_client():
    try:
        return docker.from_env()
    except Exception as e:
        logging.error(f"Error connecting to Docker daemon: {e}")
        return None

def reap_containers():
    client = get_docker_client()
    if not client:
        return
        
    try:
        containers = client.containers.list(all=True, filters={"label": "ctf_expiry"})
        current_time = int(time.time())
        
        for container in containers:
            expiry_time_str = container.labels.get("ctf_expiry")
            if not expiry_time_str:
                continue
                
            try:
                expiry_time = int(expiry_time_str)
                if current_time > expiry_time:
                    logging.info(f"Reaping expired container {container.name} (Expired at {expiry_time})")
                    container.stop()
                    container.remove()
                    
                    # Also try to remove the isolated networks
                    network_names = list(container.attrs['NetworkSettings']['Networks'].keys())
                    for network_name in network_names:
                        try:
                            client.networks.get(network_name).remove()
                            logging.info(f"Removed network {network_name}")
                        except Exception as ne:
                            logging.warning(f"Could not remove network {network_name}: {ne}")
            except ValueError:
                logging.warning(f"Invalid expiry time format on container {container.name}: {expiry_time_str}")
    except Exception as e:
        logging.error(f"Error while reaping containers: {e}")

if __name__ == "__main__":
    logging.info("Starting CTF container reaper...")
    while True:
        reap_containers()
        time.sleep(60) # Run every minute
