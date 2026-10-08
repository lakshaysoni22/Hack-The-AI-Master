"""
Lab ZIP Parser & Manifest Generator Service
=============================================
Parses uploaded ZIP files, detects lab structure, extracts metadata/storyline/missions/
questions/hints/flags, and generates a normalized internal manifest.

Supports multiple ZIP structures:
  Format A (Structured): metadata.json + storyline/ + missions/ + app/ + flags/ + questions/ + hints/
  Format B (Flat): metadata.json + missions.json + flags.json + hints.json + Dockerfile
  Format C (Flask App): app.py + Dockerfile + INSTRUCTOR.md + README.md + templates/ + static/
"""

import os
import re
import json
import uuid
import shutil
import zipfile
import logging
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of ZIP validation."""
    def __init__(self):
        self.valid = True
        self.checks = {}
        self.errors = []
        self.warnings = []

    def add_check(self, name, passed, detail=''):
        self.checks[name] = {'passed': passed, 'detail': detail}
        if not passed:
            self.valid = False
            self.errors.append(f"{name}: {detail}")

    def add_warning(self, msg):
        self.warnings.append(msg)

    def to_dict(self):
        return {
            'valid': self.valid,
            'checks': self.checks,
            'errors': self.errors,
            'warnings': self.warnings,
        }


class LabManifest:
    """Normalized lab manifest generated from parsed ZIP."""
    def __init__(self):
        self.lab_id = ''
        self.title = 'Untitled Lab'
        self.category = 'General'
        self.difficulty = 'Beginner'
        self.concept = ''
        self.storyline = ''
        self.description = ''
        self.estimated_time = 30
        self.missions = []
        self.flags = []
        self.docker_config = {}
        self.target_app_path = ''
        self.total_points = 0

    def to_dict(self):
        return {
            'lab_id': self.lab_id,
            'title': self.title,
            'category': self.category,
            'difficulty': self.difficulty,
            'concept': self.concept,
            'storyline': self.storyline,
            'description': self.description,
            'estimated_time': self.estimated_time,
            'missions': self.missions,
            'flags': self.flags,
            'docker_config': self.docker_config,
            'target_app_path': self.target_app_path,
            'total_points': self.total_points,
        }


class LabZipParser:
    """Parses uploaded ZIP files into a normalized lab manifest."""

    # Dangerous file extensions that should never be executed directly
    BLOCKED_EXTENSIONS = {'.exe', '.bat', '.cmd', '.com', '.scr', '.pif', '.msi'}

    def __init__(self, max_decompressed_size=500*1024*1024, max_file_count=10000):
        self.max_decompressed_size = max_decompressed_size
        self.max_file_count = max_file_count

    def validate_zip(self, zip_file_path):
        """Validate a ZIP file for safety and structure.
        
        Args:
            zip_file_path: Path to the uploaded ZIP file on disk.
            
        Returns:
            ValidationResult with checks and any errors.
        """
        result = ValidationResult()

        # Check file exists
        if not os.path.isfile(zip_file_path):
            result.add_check('file_exists', False, 'ZIP file not found')
            return result
        result.add_check('file_exists', True)

        # Check it's a valid ZIP
        if not zipfile.is_zipfile(zip_file_path):
            result.add_check('valid_zip', False, 'File is not a valid ZIP archive')
            return result
        result.add_check('valid_zip', True)

        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zf:
                # Path traversal protection
                has_traversal = False
                for name in zf.namelist():
                    # Check for path traversal
                    if '..' in name or name.startswith('/') or name.startswith('\\'):
                        has_traversal = True
                        break
                    # Normalize and check
                    normalized = os.path.normpath(name)
                    if normalized.startswith('..'):
                        has_traversal = True
                        break

                if has_traversal:
                    result.add_check('path_safety', False, 'ZIP contains path traversal sequences')
                    return result
                result.add_check('path_safety', True)

                # File count check
                file_count = len(zf.namelist())
                if file_count > self.max_file_count:
                    result.add_check('file_count', False, f'Too many files: {file_count} > {self.max_file_count}')
                    return result
                result.add_check('file_count', True, f'{file_count} files')

                # Decompressed size check (ZIP bomb protection)
                total_size = sum(info.file_size for info in zf.infolist())
                if total_size > self.max_decompressed_size:
                    size_mb = total_size / (1024 * 1024)
                    result.add_check('decompressed_size', False,
                                     f'Decompressed size too large: {size_mb:.1f}MB > {self.max_decompressed_size/(1024*1024):.0f}MB')
                    return result
                result.add_check('decompressed_size', True, f'{total_size/(1024*1024):.1f}MB')

                # Blocked file types
                blocked_found = []
                for name in zf.namelist():
                    ext = os.path.splitext(name)[1].lower()
                    if ext in self.BLOCKED_EXTENSIONS:
                        blocked_found.append(name)

                if blocked_found:
                    result.add_check('file_types', False,
                                     f'Blocked file types found: {", ".join(blocked_found[:5])}')
                else:
                    result.add_check('file_types', True)

                # Detect structure
                names = set(zf.namelist())
                structure = self._detect_structure_from_names(names)
                result.add_check('structure_detected', True, structure)

                # Check for key components
                has_dockerfile = any(n.lower().endswith('dockerfile') for n in names)
                has_docker_compose = any('docker-compose' in n.lower() for n in names)
                has_readme = any(n.lower().endswith('readme.md') for n in names)
                has_metadata = any(n.lower().endswith('metadata.json') for n in names)
                has_app = any(n.lower().endswith('app.py') for n in names)
                has_instructor = any('instructor' in n.lower() for n in names)

                if not (has_dockerfile or has_docker_compose):
                    result.add_warning('No Docker config found (Dockerfile or docker-compose.yml)')
                result.add_check('dockerfile_detected', True,
                                 'Dockerfile found' if has_dockerfile else
                                 'docker-compose.yml found' if has_docker_compose else 'No Docker config (Ignored)')
                                 
                if not has_readme:
                    result.add_warning('No README.md found')
                result.add_check('readme_detected', True,
                                 'README.md found' if has_readme else 'No README (Ignored)')
                
                if has_metadata:
                    result.add_check('metadata_detected', True, 'metadata.json found')
                elif has_instructor:
                    result.add_check('metadata_detected', True, 'INSTRUCTOR.md found (will extract metadata)')
                elif has_readme:
                    result.add_check('metadata_detected', True, 'Will extract metadata from README')
                else:
                    result.add_check('metadata_detected', False, 'No metadata source found')
                    result.add_warning('No metadata.json, INSTRUCTOR.md, or README.md found')

                # Check for mission/storyline content
                has_missions_dir = any(('/missions/' in n or n.startswith('missions/')) for n in names)
                has_missions_json = any(n.lower().endswith('missions.json') for n in names)
                has_storyline = any(('/storyline/' in n or n.startswith('storyline/') or
                                     'storyline' in n.lower()) for n in names)

                if has_missions_dir or has_missions_json or has_instructor:
                    result.add_check('missions_detected', True)
                else:
                    result.add_check('missions_detected', True,
                                     'No explicit missions directory; will generate from metadata')
                    result.add_warning('Missions will be auto-generated from available content')

                if has_storyline or has_instructor or has_readme:
                    result.add_check('storyline_detected', True)
                else:
                    result.add_check('storyline_detected', False, 'No storyline content found')
                    result.add_warning('No storyline found; lab will have a generic description')

                result.add_check('target_app_detected', has_app or has_dockerfile,
                                 'Target application found' if has_app else 'Docker config found')

        except zipfile.BadZipFile:
            result.add_check('valid_zip', False, 'Corrupted ZIP file')
        except Exception as e:
            result.add_check('parse_error', False, str(e))

        return result

    def parse_zip(self, zip_file_path, extract_to):
        """Parse a ZIP file and generate a normalized lab manifest.
        
        Args:
            zip_file_path: Path to the ZIP file.
            extract_to: Directory to extract ZIP contents into.
            
        Returns:
            LabManifest object with all parsed data.
        """
        os.makedirs(extract_to, exist_ok=True)

        # Safe extraction
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            for member in zf.infolist():
                # Skip directories
                if member.is_dir():
                    continue
                # Path traversal check
                member_path = os.path.normpath(member.filename)
                if member_path.startswith('..') or os.path.isabs(member_path):
                    logger.warning(f"Skipping potentially unsafe path: {member.filename}")
                    continue
                zf.extract(member, extract_to)

        # Detect the actual root directory (ZIPs often have a single root folder)
        root = self._find_lab_root(extract_to)
        logger.info(f"Lab root directory: {root}")

        # Detect structure type
        structure = self._detect_structure(root)
        logger.info(f"Detected lab structure: {structure}")

        # Build manifest based on structure
        manifest = LabManifest()
        manifest.lab_id = f"ulab-{uuid.uuid4().hex[:8]}"

        # Extract metadata
        metadata = self._extract_metadata(root, structure)
        manifest.title = metadata.get('title', metadata.get('name', 'Untitled Lab'))
        manifest.category = metadata.get('category', metadata.get('topic', 'General'))
        manifest.difficulty = metadata.get('difficulty', 'Beginner')
        manifest.concept = metadata.get('concept', metadata.get('vulnerability', ''))
        manifest.estimated_time = metadata.get('estimated_time', 30)
        manifest.description = metadata.get('description', '')

        # Extract storyline
        manifest.storyline = self._extract_storyline(root, structure, metadata)

        # Extract missions
        manifest.missions = self._extract_missions(root, structure, metadata)

        # Extract flags
        manifest.flags = self._extract_flags(root, structure, metadata)

        # Detect Docker config
        manifest.docker_config = self._detect_docker_config(root)

        # Detect target app path (relative to the extracted root)
        manifest.target_app_path = self._detect_target_app(root, extract_to)

        # Calculate total points
        manifest.total_points = sum(m.get('points', 100) for m in manifest.missions)
        for flag in manifest.flags:
            manifest.total_points += flag.get('points', 100)

        return manifest

    def _find_lab_root(self, extract_dir):
        """Find the actual root of the lab content (handle single-folder ZIPs)."""
        entries = os.listdir(extract_dir)
        # Filter out __pycache__ and hidden files
        entries = [e for e in entries if not e.startswith('.') and e != '__pycache__']

        if len(entries) == 1:
            single = os.path.join(extract_dir, entries[0])
            if os.path.isdir(single):
                # Check if this single dir has lab content
                sub_entries = os.listdir(single)
                sub_entries = [e for e in sub_entries if not e.startswith('.') and e != '__pycache__']
                # If the single dir contains another single dir (double-wrapped), unwrap again
                if len(sub_entries) == 1 and os.path.isdir(os.path.join(single, sub_entries[0])):
                    deeper = os.path.join(single, sub_entries[0])
                    deeper_entries = os.listdir(deeper)
                    if any(f.lower() in ('app.py', 'dockerfile', 'metadata.json', 'readme.md')
                           for f in deeper_entries):
                        return deeper
                # Otherwise check if this single dir is the root
                if any(f.lower() in ('app.py', 'dockerfile', 'metadata.json', 'readme.md',
                                      'instructor.md', 'docker-compose.yml')
                       for f in sub_entries):
                    return single

        return extract_dir

    def _detect_structure_from_names(self, names):
        """Detect structure type from ZIP file names."""
        has_missions_dir = any(('/missions/' in n or n.startswith('missions/')) for n in names)
        has_metadata_json = any(n.lower().endswith('metadata.json') for n in names)
        has_missions_json = any(n.lower().endswith('missions.json') for n in names)
        has_instructor_md = any('instructor' in n.lower() and n.endswith('.md') for n in names)
        has_app_py = any(n.lower().endswith('app.py') for n in names)

        if has_missions_dir and has_metadata_json:
            return 'structured'
        elif has_missions_json and has_metadata_json:
            return 'flat'
        elif has_instructor_md and has_app_py:
            return 'flask_app'
        elif has_app_py:
            return 'app_only'
        elif has_metadata_json:
            return 'metadata_only'
        else:
            return 'unknown'

    def _detect_structure(self, root):
        """Detect the lab structure type from extracted files."""
        if not os.path.isdir(root):
            return 'unknown'

        files = set()
        dirs = set()
        for entry in os.listdir(root):
            path = os.path.join(root, entry)
            if os.path.isfile(path):
                files.add(entry.lower())
            elif os.path.isdir(path):
                dirs.add(entry.lower())

        if 'missions' in dirs and 'metadata.json' in files:
            return 'structured'
        elif 'missions.json' in files and 'metadata.json' in files:
            return 'flat'
        elif ('instructor.md' in files or 'INSTRUCTOR.md' in {e for e in os.listdir(root) if os.path.isfile(os.path.join(root, e))}) and 'app.py' in files:
            return 'flask_app'
        elif 'app.py' in files:
            return 'app_only'
        elif 'metadata.json' in files:
            return 'metadata_only'
        else:
            return 'unknown'

    def _extract_metadata(self, root, structure):
        """Extract metadata from various sources."""
        metadata = {}

        # Try metadata.json first
        metadata_path = os.path.join(root, 'metadata.json')
        if os.path.isfile(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                logger.info("Loaded metadata from metadata.json")
                return metadata
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to parse metadata.json: {e}")

        # Try INSTRUCTOR.md
        for fname in os.listdir(root):
            if fname.lower() == 'instructor.md':
                instructor_path = os.path.join(root, fname)
                metadata = self._parse_instructor_md(instructor_path)
                if metadata:
                    logger.info("Extracted metadata from INSTRUCTOR.md")
                    return metadata

        # Try README.md
        for fname in os.listdir(root):
            if fname.lower() == 'readme.md':
                readme_path = os.path.join(root, fname)
                metadata = self._parse_readme_md(readme_path)
                if metadata:
                    logger.info("Extracted metadata from README.md")
                    return metadata

        return metadata

    def _parse_instructor_md(self, filepath):
        """Parse INSTRUCTOR.md for lab metadata."""
        metadata = {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title from first heading
            title_match = re.search(r'#\s+(.+?)(?:\n|$)', content)
            if title_match:
                title = title_match.group(1).strip()
                # Clean up titles like "INSTRUCTOR GUIDE (Do not distribute...)"
                if 'instructor' in title.lower():
                    # Look for a lab name in the content
                    name_match = re.search(r'(?:lab|name|title)[:\s]+["\']?([^"\'\n]+)', content, re.I)
                    if name_match:
                        title = name_match.group(1).strip()
                metadata['title'] = title

            # Extract vulnerability/concept
            vuln_match = re.search(r'(?:vulnerability|intended vulnerability)[:\s]*\n+\*\*(?:Class|Type)[:\s]*\*\*\s*(.+?)(?:\n|—)', content, re.I)
            if vuln_match:
                metadata['concept'] = vuln_match.group(1).strip()
            else:
                vuln_match = re.search(r'(?:vulnerability|concept)[:\s]+(.+?)(?:\n|$)', content, re.I)
                if vuln_match:
                    metadata['concept'] = vuln_match.group(1).strip()

            # Extract flag
            flag_match = re.search(r'(?:flag|FLAG)[:\s]*\n*```\n?(.+?)\n?```', content, re.S)
            if flag_match:
                metadata['flag'] = flag_match.group(1).strip()
            else:
                flag_match = re.search(r'FLAG:\s*(.+?)(?:\n|$)', content)
                if flag_match:
                    metadata['flag'] = flag_match.group(1).strip()

            # Extract mission solutions/answers
            missions = []
            mission_section = re.search(r'(?:Mission Solutions|Expected.*Path|Exploitation Path)(.*?)(?=##|\Z)',
                                         content, re.S | re.I)
            if mission_section:
                mission_text = mission_section.group(1)
                steps = re.findall(r'(\d+)\.\s+(.+?)(?=\n\d+\.|\Z)', mission_text, re.S)
                for num, desc in steps:
                    missions.append({
                        'mission_number': int(num),
                        'title': desc.strip().split('\n')[0][:100],
                        'objective': desc.strip(),
                    })

            if missions:
                metadata['missions_from_instructor'] = missions

            # Extract knowledge check answers
            kc_section = re.search(r'(?:Knowledge Check|Mission.*Answers)(.*?)(?=##|\Z)', content, re.S | re.I)
            if kc_section:
                metadata['knowledge_check_raw'] = kc_section.group(1).strip()

            # Detect category from content
            if any(term in content.lower() for term in ['xss', 'cross-site scripting']):
                metadata['category'] = 'Web Security'
                metadata.setdefault('concept', 'Cross-Site Scripting (XSS)')
            elif any(term in content.lower() for term in ['access control', 'authorization', 'broken access']):
                metadata['category'] = 'Web Security'
                metadata.setdefault('concept', 'Broken Access Control')
            elif any(term in content.lower() for term in ['sql injection', 'sqli']):
                metadata['category'] = 'Web Security'
                metadata.setdefault('concept', 'SQL Injection')
            elif any(term in content.lower() for term in ['idor', 'insecure direct']):
                metadata['category'] = 'Web Security'
                metadata.setdefault('concept', 'IDOR')

            # Set difficulty based on content indicators
            if any(term in content.lower() for term in ['beginner', 'basic', 'introductory']):
                metadata['difficulty'] = 'Beginner'
            elif any(term in content.lower() for term in ['intermediate', 'moderate', 'pro']):
                metadata['difficulty'] = 'Pro'
            elif any(term in content.lower() for term in ['advanced', 'expert', 'hard']):
                metadata['difficulty'] = 'Advanced'

        except IOError as e:
            logger.warning(f"Failed to read INSTRUCTOR.md: {e}")

        return metadata

    def _parse_readme_md(self, filepath):
        """Parse README.md for basic lab metadata."""
        metadata = {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title
            title_match = re.search(r'#\s+(.+?)(?:\n|$)', content)
            if title_match:
                metadata['title'] = title_match.group(1).strip()

            # Extract description (first paragraph after title)
            desc_match = re.search(r'#.+?\n\n(.+?)(?:\n\n|\n#)', content, re.S)
            if desc_match:
                metadata['description'] = desc_match.group(1).strip()[:500]

        except IOError:
            pass

        return metadata

    def _extract_storyline(self, root, structure, metadata):
        """Extract storyline content from various sources."""
        # Check for storyline directory
        storyline_dir = os.path.join(root, 'storyline')
        if os.path.isdir(storyline_dir):
            parts = []
            for fname in sorted(os.listdir(storyline_dir)):
                fpath = os.path.join(storyline_dir, fname)
                if os.path.isfile(fpath) and fname.endswith('.md'):
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            parts.append(f.read().strip())
                    except IOError:
                        pass
            if parts:
                return '\n\n'.join(parts)

        # Check for storyline.md or storyline.json
        for fname in ('storyline.md', 'storyline.json', 'story.md'):
            fpath = os.path.join(root, fname)
            if os.path.isfile(fpath):
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    if fname.endswith('.json'):
                        data = json.loads(content)
                        return data.get('storyline', data.get('story', json.dumps(data)))
                    return content
                except (IOError, json.JSONDecodeError):
                    pass

        # Extract from README.md
        readme_path = None
        for fname in os.listdir(root):
            if fname.lower() == 'readme.md':
                readme_path = os.path.join(root, fname)
                break

        if readme_path:
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Look for a story/scenario section
                story_match = re.search(
                    r'(?:##?\s*(?:Story|Scenario|Background|Context|Storyline))\s*\n(.*?)(?=\n##|\Z)',
                    content, re.S | re.I)
                if story_match:
                    return story_match.group(1).strip()
                # Otherwise use the description/intro
                intro_match = re.search(r'#.+?\n\n(.+?)(?:\n\n#|\Z)', content, re.S)
                if intro_match:
                    return intro_match.group(1).strip()
            except IOError:
                pass

        # From metadata
        if metadata.get('storyline'):
            return metadata['storyline']
        if metadata.get('description'):
            return metadata['description']

        return ''

    def _extract_missions(self, root, structure, metadata):
        """Extract missions from various sources."""
        missions = []

        # Method 1: missions directory with individual files
        missions_dir = os.path.join(root, 'missions')
        if os.path.isdir(missions_dir):
            missions = self._parse_missions_directory(missions_dir)
            if missions:
                return missions

        # Method 2: missions.json
        missions_json = os.path.join(root, 'missions.json')
        if os.path.isfile(missions_json):
            try:
                with open(missions_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    missions = data
                elif isinstance(data, dict) and 'missions' in data:
                    missions = data['missions']
                if missions:
                    return self._normalize_missions(missions)
            except (json.JSONDecodeError, IOError):
                pass

        # Method 3: From metadata (INSTRUCTOR.md extracted missions)
        if metadata.get('missions_from_instructor'):
            raw = metadata['missions_from_instructor']
            return self._normalize_missions(raw)

        # Method 4: From metadata.json missions field
        if metadata.get('missions'):
            return self._normalize_missions(metadata['missions'])

        # Method 5: Auto-generate a single mission from available info
        logger.info("No explicit missions found; generating default mission structure")
        return [{
            'mission_number': 1,
            'title': 'Explore the Application',
            'objective': metadata.get('description', 'Explore the target application and find the vulnerability.'),
            'instructions': ['Examine the target application in the right panel.',
                             'Look for potential security vulnerabilities.',
                             'Complete the objective and submit the flag.'],
            'questions': [],
            'hints': [],
            'points': 100,
        }]

    def _parse_missions_directory(self, missions_dir):
        """Parse a missions/ directory containing individual mission files."""
        missions = []
        for fname in sorted(os.listdir(missions_dir)):
            fpath = os.path.join(missions_dir, fname)
            if fname.endswith('.json') and os.path.isfile(fpath):
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        mission = json.load(f)
                    missions.append(mission)
                except (json.JSONDecodeError, IOError):
                    pass
            elif fname.endswith('.md') and os.path.isfile(fpath):
                mission = self._parse_mission_md(fpath, len(missions) + 1)
                if mission:
                    missions.append(mission)

        return self._normalize_missions(missions) if missions else []

    def _parse_mission_md(self, filepath, number):
        """Parse a mission markdown file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            mission = {'mission_number': number}

            # Title from first heading
            title_match = re.search(r'#\s+(.+?)(?:\n|$)', content)
            if title_match:
                mission['title'] = title_match.group(1).strip()

            # Objective
            obj_match = re.search(r'(?:##?\s*Objective)\s*\n(.+?)(?=\n##|\Z)', content, re.S | re.I)
            if obj_match:
                mission['objective'] = obj_match.group(1).strip()

            # Instructions
            inst_match = re.search(r'(?:##?\s*Instructions?)\s*\n(.+?)(?=\n##|\Z)', content, re.S | re.I)
            if inst_match:
                instructions = re.findall(r'[-*]\s+(.+)', inst_match.group(1))
                if not instructions:
                    instructions = [inst_match.group(1).strip()]
                mission['instructions'] = instructions

            # Questions
            q_match = re.search(r'(?:##?\s*Questions?)\s*\n(.+?)(?=\n##|\Z)', content, re.S | re.I)
            if q_match:
                questions = []
                q_items = re.findall(r'[-*]\s+(.+?)(?:\n|$)', q_match.group(1))
                for q_text in q_items:
                    # Try to extract answer hint like "Answer: something"
                    parts = re.split(r'\s*[|:]\s*(?:answer|ans)\s*[=:]\s*', q_text, flags=re.I)
                    q_entry = {'question': parts[0].strip()}
                    if len(parts) > 1:
                        q_entry['answer'] = parts[1].strip()
                    questions.append(q_entry)
                mission['questions'] = questions

            # Hints
            h_match = re.search(r'(?:##?\s*Hints?)\s*\n(.+?)(?=\n##|\Z)', content, re.S | re.I)
            if h_match:
                hints = re.findall(r'[-*]\s+(.+)', h_match.group(1))
                mission['hints'] = [{'hint_text': h.strip()} for h in hints]

            return mission
        except IOError:
            return None

    def _normalize_missions(self, raw_missions):
        """Normalize missions to a consistent format."""
        normalized = []
        for i, m in enumerate(raw_missions):
            mission = {
                'mission_number': m.get('mission_number', m.get('number', i + 1)),
                'title': m.get('title', f'Mission {i + 1}'),
                'objective': m.get('objective', m.get('description', '')),
                'instructions': m.get('instructions', []),
                'storyline_text': m.get('storyline_text', m.get('storyline', m.get('story', ''))),
                'target_url_path': m.get('target_url', m.get('target_url_path', '')),
                'points': m.get('points', 100),
                'questions': [],
                'hints': [],
            }

            # Normalize instructions to a list
            if isinstance(mission['instructions'], str):
                mission['instructions'] = [mission['instructions']]

            # Normalize questions
            raw_questions = m.get('questions', [])
            for j, q in enumerate(raw_questions):
                if isinstance(q, str):
                    question = {'question': q, 'answer': '', 'validation_type': 'ANSWER_MATCH'}
                elif isinstance(q, dict):
                    question = {
                        'question': q.get('question', q.get('text', '')),
                        'answer': q.get('answer', q.get('expected', q.get('expected_answer', ''))),
                        'validation_type': q.get('validation_type', q.get('type', 'ANSWER_MATCH')),
                        'case_sensitive': q.get('case_sensitive', False),
                        'explanation': q.get('explanation', ''),
                        'xp_reward': q.get('xp_reward', q.get('points', 100)),
                    }
                else:
                    continue
                mission['questions'].append(question)

            # Normalize hints
            raw_hints = m.get('hints', [])
            for h in raw_hints:
                if isinstance(h, str):
                    mission['hints'].append({'hint_text': h, 'xp_cost': 10})
                elif isinstance(h, dict):
                    mission['hints'].append({
                        'hint_text': h.get('hint_text', h.get('text', '')),
                        'xp_cost': h.get('xp_cost', h.get('cost', 10)),
                    })

            normalized.append(mission)

        # Sort by mission number
        normalized.sort(key=lambda m: m['mission_number'])
        return normalized

    def _extract_flags(self, root, structure, metadata):
        """Extract flags from various sources."""
        flags = []

        # From flags directory
        flags_dir = os.path.join(root, 'flags')
        if os.path.isdir(flags_dir):
            for fname in os.listdir(flags_dir):
                fpath = os.path.join(flags_dir, fname)
                if fname.endswith('.json') and os.path.isfile(fpath):
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        if isinstance(data, list):
                            flags.extend(data)
                        elif isinstance(data, dict):
                            flags.append(data)
                    except (json.JSONDecodeError, IOError):
                        pass

        # From flags.json
        flags_json = os.path.join(root, 'flags.json')
        if os.path.isfile(flags_json) and not flags:
            try:
                with open(flags_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    flags = data
                elif isinstance(data, dict):
                    if 'flags' in data:
                        flags = data['flags']
                    else:
                        flags = [data]
            except (json.JSONDecodeError, IOError):
                pass

        # From metadata
        if not flags and metadata.get('flag'):
            flags = [{'flag_value': metadata['flag'], 'description': 'Main flag'}]

        if not flags and metadata.get('flags'):
            raw = metadata['flags']
            if isinstance(raw, list):
                flags = raw
            elif isinstance(raw, str):
                flags = [{'flag_value': raw}]

        # Normalize
        normalized = []
        for f in flags:
            if isinstance(f, str):
                normalized.append({'flag_value': f, 'description': '', 'points': 100})
            elif isinstance(f, dict):
                normalized.append({
                    'flag_value': f.get('flag_value', f.get('value', f.get('flag', ''))),
                    'description': f.get('description', f.get('flag_description', '')),
                    'mission_id': f.get('mission_id', None),
                    'points': f.get('points', 100),
                })

        return normalized

    def _detect_docker_config(self, root):
        """Detect Docker configuration in the lab."""
        config = {
            'has_dockerfile': False,
            'has_compose': False,
            'dockerfile_path': None,
            'compose_path': None,
            'ports': [],
        }

        # Walk directory tree to find Docker files
        for dirpath, dirnames, filenames in os.walk(root):
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(fpath, root)

                if fname.lower() == 'dockerfile':
                    config['has_dockerfile'] = True
                    config['dockerfile_path'] = rel_path
                    # Try to extract exposed ports
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        ports = re.findall(r'EXPOSE\s+(\d+)', content)
                        config['ports'].extend([int(p) for p in ports])
                    except IOError:
                        pass

                elif 'docker-compose' in fname.lower() and (fname.endswith('.yml') or fname.endswith('.yaml')):
                    config['has_compose'] = True
                    config['compose_path'] = rel_path

        # Default port if none detected
        if not config['ports']:
            config['ports'] = [5000]  # Default Flask port

        return config

    def _detect_target_app(self, root, extract_base):
        """Detect the target application path relative to extract_base."""
        # The target app is wherever the Dockerfile or app.py lives
        for dirpath, dirnames, filenames in os.walk(root):
            lower_files = {f.lower(): f for f in filenames}
            if 'dockerfile' in lower_files or 'app.py' in lower_files:
                return os.path.relpath(dirpath, extract_base)

        return os.path.relpath(root, extract_base)


def save_manifest_to_db(manifest, extract_path, user_id=None):
    """Save a parsed lab manifest to the database.
    
    Args:
        manifest: LabManifest object
        extract_path: Path where ZIP was extracted
        user_id: ID of the admin who uploaded
        
    Returns:
        UploadedLab database object
    """
    from extensions import db
    from models import (UploadedLab, UploadedLabMission, UploadedLabQuestion,
                        UploadedLabHint, UploadedLabFlag)

    # New labs are appended after every existing lab by default, so the
    # learning path stays sequential without an admin having to set this
    # manually for every upload. An admin can still edit sort_order later
    # to reorder the path.
    max_order = db.session.query(db.func.max(UploadedLab.sort_order)).scalar() or 0

    lab = UploadedLab(
        id=manifest.lab_id,
        title=manifest.title,
        category=manifest.category,
        difficulty=manifest.difficulty,
        concept=manifest.concept,
        storyline=manifest.storyline,
        description=manifest.description,
        estimated_time=manifest.estimated_time,
        total_points=manifest.total_points,
        status='draft',
        zip_path=extract_path,
        docker_config=json.dumps(manifest.docker_config),
        target_app_path=manifest.target_app_path,
        manifest_json=json.dumps(manifest.to_dict()),
        created_by=user_id,
        sort_order=max_order + 1,
    )
    db.session.add(lab)

    # Save missions
    for m in manifest.missions:
        mission_id = f"{manifest.lab_id}_m{m['mission_number']}"
        mission = UploadedLabMission(
            id=mission_id,
            lab_id=manifest.lab_id,
            mission_number=m['mission_number'],
            title=m['title'],
            objective=m.get('objective', ''),
            instructions=json.dumps(m.get('instructions', [])),
            storyline_text=m.get('storyline_text', ''),
            target_url_path=m.get('target_url_path', ''),
            points=m.get('points', 100),
        )
        db.session.add(mission)

        # Save questions for this mission
        for qi, q in enumerate(m.get('questions', [])):
            q_id = f"{mission_id}_q{qi + 1}"
            question = UploadedLabQuestion(
                id=q_id,
                mission_id=mission_id,
                question_text=q.get('question', ''),
                validation_type=q.get('validation_type', 'ANSWER_MATCH'),
                expected_answer=q.get('answer', ''),
                case_sensitive=q.get('case_sensitive', False),
                explanation=q.get('explanation', ''),
                xp_reward=q.get('xp_reward', 100),
                sort_order=qi + 1,
            )
            db.session.add(question)

        # Save hints for this mission
        for hi, h in enumerate(m.get('hints', [])):
            h_id = f"{mission_id}_h{hi + 1}"
            hint = UploadedLabHint(
                id=h_id,
                mission_id=mission_id,
                hint_text=h.get('hint_text', ''),
                xp_cost=h.get('xp_cost', 10),
                sort_order=hi + 1,
            )
            db.session.add(hint)

    # Save flags
    for fi, f_data in enumerate(manifest.flags):
        flag_id = f"{manifest.lab_id}_f{fi + 1}"
        flag = UploadedLabFlag(
            id=flag_id,
            lab_id=manifest.lab_id,
            mission_id=f_data.get('mission_id'),
            flag_value=f_data.get('flag_value', ''),
            flag_description=f_data.get('description', ''),
            points=f_data.get('points', 100),
        )
        db.session.add(flag)

    db.session.flush()
    return lab
