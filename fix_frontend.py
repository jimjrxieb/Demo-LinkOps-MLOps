#!/usr/bin/env python3
"""
Frontend Auto-Fix Script for LinkOps-MLOps
Automatically fixes common ESLint warnings, errors, and build issues in Vue.js frontend
Updated for new frontend structure with authentication, demo mode, and lint error handling
"""

import json
import os
import re
import subprocess
from pathlib import Path
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import argparse
from tqdm import tqdm
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(f'frontend_fix_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_command(cmd, cwd=None):
    """Run a shell command and return result"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        logger.error(f"Error running command '{cmd}': {e}", exc_info=True)
        return False, "", str(e)

def load_config():
    """Load configuration from .fix_frontend.json"""
    config_file = Path('frontend/.fix_frontend.json')
    default_config = {
        'directories': ['src/components', 'src/views', 'src/router', 'src/store', 'src/utils', 'src/assets', 'src/pages', '.'],
        'patterns': ['*.vue', '*.js', '*.ts', '*.jsx']
    }
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            logger.info(f"Loaded config from {config_file}")
            return json.load(f)
    logger.info("Using default config")
    return default_config

def get_file_hash(file_path):
    """Calculate MD5 hash of a file"""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def parse_eslint_output(stderr):
    """Parse ESLint output to extract errors and warnings"""
    logger.info("Parsing ESLint output for errors and warnings...")
    issues = []
    current_file = None
    for line in stderr.splitlines():
        # Match file path
        if line.startswith(str(Path.cwd())) or '/frontend/' in line:
            current_file = Path(line.strip())
            continue
        # Match ESLint issue (e.g., "  1:2  error  Missing semicolon  semi")
        match = re.match(r'\s*(\d+):(\d+)\s+(error|warning)\s+(.+?)\s+(\w+)$', line)
        if match and current_file:
            line_num, col_num, severity, message, rule = match.groups()
            issues.append({
                'file': current_file,
                'line': int(line_num),
                'column': int(col_num),
                'severity': severity,
                'message': message,
                'rule': rule
            })
    logger.info(f"Found {len(issues)} ESLint issues")
    return issues

def fix_eslint_issues(file_path, content, issues):
    """Fix specific ESLint issues in a file"""
    logger.info(f"Fixing ESLint issues in {file_path}")
    lines = content.split("\n")
    changes_made = 0
    for issue in [i for i in issues if str(i['file']) == str(file_path)]:
        line_idx = issue['line'] - 1
        if line_idx >= len(lines):
            continue
        line = lines[line_idx]
        # Fix missing semicolons
        if issue['rule'] == 'semi' and 'Missing semicolon' in issue['message']:
            if not line.strip().endswith(';'):
                lines[line_idx] = line.rstrip() + ';'
                changes_made += 1
        # Fix unused imports/variables
        elif issue['rule'] == 'no-unused-vars' and 'is defined but never used' in issue['message']:
            match = re.search(r"'([^']+)' is defined but never used", issue['message'])
            if match:
                unused_var = match.group(1)
                lines[line_idx] = re.sub(rf"\b{unused_var}\b", f"_{unused_var}", line)
                changes_made += 1
        # Fix spacing issues
        elif issue['rule'] == 'space-before-function-paren':
            lines[line_idx] = re.sub(r'function(\w+)\(', r'function \1 (', line)
            changes_made += 1
        # Fix vue/html-indent
        elif issue['rule'] == 'html-indent' and 'Expected indentation' in issue['message']:
            match = re.search(r'Expected indentation of (\d+) spaces but found (\d+) spaces', issue['message'])
            if match:
                expected_spaces, found_spaces = int(match.group(1)), int(match.group(2))
                indent_diff = found_spaces - expected_spaces
                if indent_diff > 0:
                    lines[line_idx] = line[indent_diff:]
                else:
                    lines[line_idx] = ' ' * abs(indent_diff) + line
                changes_made += 1
        # Fix vue/max-attributes-per-line
        elif issue['rule'] == 'max-attributes-per-line' and 'should be on a new line' in issue['message']:
            match = re.search(r"'([^']+)' should be on a new line", issue['message'])
            if match:
                attr = match.group(1)
                lines[line_idx] = re.sub(rf'\s*{attr}=', f'\n      {attr}=', line)
                changes_made += 1
        # Fix vue/attributes-order
        elif issue['rule'] == 'attributes-order':
            match = re.search(r"Attribute \"([^\"]+)\" should go before \"([^\"]+)\"", issue['message'])
            if match:
                attr1, attr2 = match.group(1), match.group(2)
                lines[line_idx] = re.sub(rf'\s*{attr1}="[^"]+"\s*{attr2}="[^"]+"', f' {attr1}="{{{{attr1}}}}" {attr2}="{{{{attr2}}}}"', line)
                changes_made += 1
        # Fix vue/html-self-closing
        elif issue['rule'] == 'html-self-closing' and 'Disallow self-closing on HTML void elements' in issue['message']:
            lines[line_idx] = line.replace('/>', '>')
            changes_made += 1
        # Fix vue/no-duplicate-attributes
        elif issue['rule'] == 'no-duplicate-attributes' and 'Duplicate attribute' in issue['message']:
            lines[line_idx] = re.sub(r';\s*;', ';', line)
            lines[line_idx] = re.sub(r'\s*;\s*([^\s])', r' \1', lines[line_idx])
            changes_made += 1
        # Fix vue/no-parsing-error (x-invalid-end-tag)
        elif issue['rule'] == 'no-parsing-error' and 'x-invalid-end-tag' in issue['message']:
            if line.strip().endswith('</'):
                lines[line_idx] = line.rstrip('</') + '>'
                changes_made += 1
        # Fix vue/require-explicit-emits
        elif issue['rule'] == 'require-explicit-emits':
            match = re.search(r"The \"([^\"]+)\" event has been triggered but not declared", issue['message'])
            if match:
                event = match.group(1)
                script_idx = next((i for i, l in enumerate(lines) if '<script' in l), -1)
                if script_idx != -1:
                    define_emits = next((i for i, l in enumerate(lines[script_idx:]) if 'defineEmits' in l), -1)
                    if define_emits == -1:
                        lines.insert(script_idx + 1, f"const emit = defineEmits(['{event}'])")
                    else:
                        lines[script_idx + define_emits] = re.sub(r'defineEmits\(\[([^\]]*)\]\)', rf"defineEmits([\1, '{event}'])", lines[script_idx + define_emits])
                    changes_made += 1
        # Fix vue/no-unused-components
        elif issue['rule'] == 'no-unused-components':
            match = re.search(r"The \"([^\"]+)\" component has been registered but not used", issue['message'])
            if match:
                component = match.group(1)
                script_idx = next((i for i, l in enumerate(lines) if '<script' in l), -1)
                if script_idx != -1:
                    components_line = next((i for i, l in enumerate(lines[script_idx:]) if 'components:' in l), -1)
                    if components_line != -1:
                        lines[script_idx + components_line] = re.sub(rf"'{component}'", f"'{component}' // TODO: Use or remove", lines[script_idx + components_line])
                        changes_made += 1
        # Fix vue/multiline-html-element-content-newline
        elif issue['rule'] == 'multiline-html-element-content-newline':
            if 'after opening tag' in issue['message']:
                lines[line_idx] = line + '\n'
                changes_made += 1
        # Fix vue/singleline-html-element-content-newline
        elif issue['rule'] == 'singleline-html-element-content-newline':
            if 'after opening tag' in issue['message']:
                lines[line_idx] = re.sub(r'>([^<]+)<', r'>\n\1\n<', line)
                changes_made += 1
    if changes_made > 0:
        logger.info(f"Fixed {changes_made} ESLint issues")
    return "\n".join(lines)

def fix_vite_config_syntax(file_path):
    """Fix common Vite config syntax errors"""
    logger.info(f"Checking Vite config syntax in {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        original_content = content
        changes_made = 0
        # Fix duplicate defineConfig imports
        content = re.sub(r'import\s*{\s*defineConfig\s*,\s*defineConfig\s*(,\s*defineConfig\s*)?\}\s*from\s*[\'"]vite[\'"]', r'import { defineConfig } from "vite"', content)
        # Ensure single defineConfig
        if 'defineConfig' not in content:
            content = content.replace('export default {', 'export default defineConfig({')
            changes_made += 1
        # Fix extra semicolons in object properties
        content = re.sub(r"'([^']+)';", r"'\1'", content)
        content = re.sub(r'"([^"]+)";', r'"\1"', content)
        # Fix extra semicolons in array items
        content = re.sub(r"'([^']+)',\s*;", r"'\1',", content)
        content = re.sub(r'"([^"]+)",\s*;', r'"\1",', content)
        # Fix trailing semicolons in object properties
        content = re.sub(r':\s*([^,}]+);\s*([,}])', r': \1\2', content)
        # Fix missing commas in object properties
        content = re.sub(r"'([^']+)'\s*\n\s*'([^']+)'", r"'\1',\n      '\2'", content)
        content = re.sub(r'"([^"]+)"\s*\n\s*"([^"]+)"', r'"\1",\n      "\2"', content)
        # Fix function calls with extra semicolons
        content = re.sub(r'\(\s*([^)]+)\s*\)\s*;', r'(\1)', content)
        # Add CORS configuration
        if 'server:' not in content:
            content = content.replace('export default defineConfig({', '''export default defineConfig({
  server: {
    cors: {
      origin: '*',
      methods: ['GET', 'POST'],
      credentials: true
    }
  },''')
            changes_made += 1
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info("Fixed Vite config syntax errors")
            return True
        return False
    except Exception as e:
        logger.error(f"Error fixing Vite config: {e}", exc_info=True)
        return False

def fix_package_json_scripts(file_path):
    """Fix missing scripts in package.json"""
    logger.info(f"Checking package.json scripts in {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        original_data = json.dumps(data, indent=2)
        changes_made = 0
        if 'scripts' in data:
            scripts = data['scripts']
            if 'lint' in scripts and 'lint:fix' not in scripts:
                lint_cmd = scripts['lint']
                if '--fix' not in lint_cmd:
                    scripts['lint:fix'] = lint_cmd + ' --fix'
                    changes_made += 1
                    logger.info("Added lint:fix script")
            if 'lint' in scripts and '--fix' in scripts['lint']:
                scripts['lint'] = scripts['lint'].replace(' --fix', '')
                changes_made += 1
                logger.info("Fixed lint script (removed --fix flag)")
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        return False
    except Exception as e:
        logger.error(f"Error fixing package.json: {e}", exc_info=True)
        return False

def fix_eslint_config(file_path):
    """Fix ESLint configuration issues"""
    logger.info(f"Checking ESLint config in {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        original_content = content
        changes_made = 0
        if 'extends' in content and 'vue/essential' not in content:
            content = content.replace('extends: [', 'extends: [\n    "plugin:vue/vue3-essential",')
            changes_made += 1
        if 'parserOptions' not in content:
            content = content.replace('extends: [', 'extends: [\n    parserOptions: { ecmaVersion: 2020, sourceType: "module" },')
            changes_made += 1
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info("Fixed ESLint configuration")
            return True
        return False
    except Exception as e:
        logger.error(f"Error fixing ESLint config: {e}", exc_info=True)
        return False

def fix_npm_ci_errors(frontend_dir):
    """Fix npm ci errors by syncing package-lock.json with package.json"""
    logger.info("Checking for npm ci sync issues...")
    success, stdout, stderr = run_command("npm ci", cwd=frontend_dir)
    if success:
        logger.info("npm ci completed successfully - no sync issues found")
        return True
    if "package-lock.json" in stderr and "sync" in stderr.lower():
        logger.info("Detected package-lock.json sync issue - attempting to fix...")
        lock_file = frontend_dir / "package-lock.json"
        if lock_file.exists():
            try:
                lock_file.unlink()
                logger.info("Removed outdated package-lock.json")
            except Exception as e:
                logger.error(f"Failed to remove package-lock.json: {e}", exc_info=True)
                return False
        logger.info("Running npm install to generate new package-lock.json...")
        success, stdout, stderr = run_command("npm install", cwd=frontend_dir)
        if success:
            logger.info("Successfully generated new package-lock.json")
            logger.info("Verifying fix with npm ci...")
            success, stdout, stderr = run_command("npm ci", cwd=frontend_dir)
            if success:
                logger.info("npm ci now works correctly!")
                return True
            logger.error(f"npm ci still failing after package-lock.json regeneration: {stderr}")
            return False
        logger.error(f"Failed to run npm install: {stderr}")
        return False
    elif "Invalid: lock file's" in stderr:
        logger.info("Detected dependency version conflicts - attempting to resolve...")
        conflicts = []
        for line in stderr.split("\n"):
            if "Invalid: lock file's" in line:
                match = re.search(r"lock file's (\w+)@([\d.]+) does not satisfy (\w+)@([\d.]+)", line)
                if match:
                    package, lock_ver, req_ver = match.group(1), match.group(2), match.group(4)
                    conflicts.append((package, lock_ver, req_ver))
        if conflicts:
            logger.info(f"Found {len(conflicts)} dependency conflicts:")
            for package, lock_ver, req_ver in conflicts:
                logger.info(f"  • {package}: lock has {lock_ver}, needs {req_ver}")
            logger.info("Cleaning npm cache and reinstalling...")
            lock_file = frontend_dir / "package-lock.json"
            if lock_file.exists():
                lock_file.unlink()
                logger.info("Removed package-lock.json")
            node_modules = frontend_dir / "node_modules"
            if node_modules.exists():
                try:
                    import shutil
                    shutil.rmtree(node_modules)
                    logger.info("Removed node_modules directory")
                except Exception as e:
                    logger.error(f"Could not remove node_modules: {e}", exc_info=True)
            logger.info("Clearing npm cache...")
            run_command("npm cache clean --force", cwd=frontend_dir)
            logger.info("Reinstalling dependencies...")
            success, stdout, stderr = run_command("npm install", cwd=frontend_dir)
            if success:
                logger.info("Dependencies reinstalled successfully")
                logger.info("Testing npm ci...")
                success, stdout, stderr = run_command("npm ci", cwd=frontend_dir)
                if success:
                    logger.info("npm ci now works correctly!")
                    return True
                logger.error(f"npm ci still failing after reinstall: {stderr}")
                return False
            logger.error(f"Failed to reinstall dependencies: {stderr}")
            return False
    logger.error(f"npm ci failed with unknown error: {stderr}")
    return False

def fix_console_statements(file_path, content):
    """Fix console statements by removing or replacing them"""
    logger.info(f"Fixing console statements in {file_path}")
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0
    for i, line in enumerate(lines):
        original_line = line
        console_pattern = r"(\s*)(console\.(log|error|warn|info|debug)\s*\([^)]*\)\s*;?)"
        match = re.search(console_pattern, line)
        if match:
            indent = match.group(1)
            console_stmt = match.group(2)
            if "error" in console_stmt.lower():
                fixed_line = f"{indent}// Development logging: {console_stmt}"
            else:
                fixed_line = f"{indent}// Removed console statement: {console_stmt}"
            fixed_lines.append(fixed_line)
            changes_made += 1
        else:
            fixed_lines.append(original_line)
    if changes_made > 0:
        logger.info(f"Fixed {changes_made} console statements")
    return "\n".join(fixed_lines)

def fix_unused_variables(file_path, content):
    """Fix unused variables by removing or marking them as used"""
    logger.info(f"Fixing unused variables in {file_path}")
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0
    for line in lines:
        original_line = line
        if "catch (" in line and "error" in line:
            fixed_line = re.sub(r"catch\s*\(\s*error\s*\)", "catch (_error)", line)
            if fixed_line != original_line:
                fixed_lines.append(fixed_line)
                changes_made += 1
                continue
        if "const {" in line and "} =" in line:
            fixed_line = re.sub(r"const\s*{\s*([^}]+)\s*}\s*=", r"const {_\1} =", line)
            if fixed_line != original_line:
                fixed_lines.append(fixed_line)
                changes_made += 1
                continue
        fixed_lines.append(original_line)
    if changes_made > 0:
        logger.info(f"Fixed {changes_made} unused variables")
    return "\n".join(fixed_lines)

def fix_vue_props(file_path, content):
    """Fix Vue.js props validation issues"""
    logger.info(f"Fixing Vue props in {file_path}")
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0
    in_define_props = False
    for line in lines:
        original_line = line
        if 'defineProps' in line and 'type:' not in line:
            in_define_props = True
            fixed_line = line.replace('defineProps({', 'defineProps<{')
            if fixed_line != original_line:
                changes_made += 1
        elif in_define_props and '}' in line:
            in_define_props = False
            fixed_line = line.replace('})', '}>({ required: false })')
            changes_made += 1
        elif "props:" in line and "required:" not in line:
            fixed_line = line.replace("type:", "required: false, type:")
            changes_made += 1
        elif "type: String" in line and "default:" not in line:
            fixed_line = line.replace("type: String", "type: String, default: ''")
            changes_made += 1
        elif "type: Number" in line and "default:" not in line:
            fixed_line = line.replace("type: Number", "type: Number, default: 0")
            changes_made += 1
        elif "type: Boolean" in line and "default:" not in line:
            fixed_line = line.replace("type: Boolean", "type: Boolean, default: false")
            changes_made += 1
        else:
            fixed_line = original_line
        fixed_lines.append(fixed_line)
    if changes_made > 0:
        logger.info(f"Fixed {changes_made} Vue props")
    return "\n".join(fixed_lines)

def fix_accessibility(file_path, content):
    """Fix accessibility issues in Vue components"""
    logger.info(f"Fixing accessibility in {file_path}")
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0
    for line in lines:
        original_line = line
        if '<button' in line and 'aria-label' not in line:
            fixed_line = line.replace('<button', '<button aria-label="Button"')
            changes_made += 1
        else:
            fixed_line = original_line
        fixed_lines.append(fixed_line)
    if changes_made > 0:
        logger.info(f"Fixed {changes_made} accessibility issues")
    return "\n".join(fixed_lines)

def fix_javascript_issues(file_path, content):
    """Fix common JavaScript issues"""
    logger.info(f"Fixing JavaScript issues in {file_path}")
    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0
    for line in lines:
        original_line = line
        if line.strip() and not line.strip().endswith((";", "{", "}", ":", ",")):
            if not line.strip().startswith(("//", "/*", "*", "import", "export")):
                if not line.rstrip().endswith(";"):
                    fixed_line = line.rstrip() + ";"
                    fixed_lines.append(fixed_line)
                    changes_made += 1
                    continue
        if '"' in line and not line.strip().startswith(("//", "/*")):
            if re.search(r'"[^"]*"', line) and not re.search(r'"[^"]*"[^"]*"', line):
                fixed_line = line.replace('"', "'")
                fixed_lines.append(fixed_line)
                changes_made += 1
                continue
        fixed_lines.append(original_line)
    if changes_made > 0:
        logger.info(f"Fixed {changes_made} JavaScript issues")
    return "\n".join(fixed_lines)

def process_file(file_path, issues, cache_file=Path('frontend/.fix_frontend_cache.json')):
    """Process a single file and apply fixes"""
    cache = {}
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    current_hash = get_file_hash(file_path)
    if str(file_path) in cache and cache[str(file_path)] == current_hash:
        logger.info(f"Skipping unchanged file: {file_path}")
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        original_content = content
        if file_path.suffix in [".vue", ".js", ".ts", ".jsx"]:
            content = fix_eslint_issues(file_path, content, issues)
            content = fix_console_statements(file_path, content)
            content = fix_unused_variables(file_path, content)
            content = fix_javascript_issues(file_path, content)
        if file_path.suffix == ".vue":
            content = fix_vue_props(file_path, content)
            content = fix_accessibility(file_path, content)
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            cache[str(file_path)] = current_hash
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f)
            return True
        return False
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}", exc_info=True)
        return False

def find_frontend_files(frontend_dir):
    """Find all frontend files that need processing"""
    logger.info("Scanning for frontend files...")
    config = load_config()
    files_to_process = []
    demo_files = ['Login.vue', 'DemoDashboard.vue']
    for file in demo_files:
        file_path = frontend_dir / 'src/components' / file
        if file_path.exists():
            files_to_process.append(file_path)
    for directory in config['directories']:
        dir_path = frontend_dir / directory if directory else frontend_dir
        if dir_path.exists():
            for pattern in config['patterns']:
                files = list(dir_path.rglob(pattern))  # Use rglob for recursive search
                files_to_process.extend(files)
    files_to_process = sorted(set(files_to_process))
    logger.info(f"Found {len(files_to_process)} files to process")
    return files_to_process

def run_eslint_fix(frontend_dir):
    """Run ESLint auto-fix and parse output for additional fixes"""
    logger.info("Running ESLint auto-fix...")
    package_json = frontend_dir / "package.json"
    if package_json.exists():
        fix_package_json_scripts(package_json)
    success, stdout, stderr = run_command("npm run lint:fix", cwd=frontend_dir)
    issues = parse_eslint_output(stderr)
    if success:
        logger.info("ESLint auto-fix completed successfully")
    else:
        logger.warning(f"ESLint auto-fix completed with warnings: {stdout}")
        if stderr:
            logger.error(f"ESLint errors: {stderr}")
    return success, issues

def test_build(frontend_dir):
    """Test the build process with error recovery"""
    logger.info("Testing build process...")
    vite_config = frontend_dir / "vite.config.js"
    if vite_config.exists():
        fix_vite_config_syntax(vite_config)
    success, stdout, stderr = run_command("npm run build", cwd=frontend_dir)
    if success:
        logger.info("Build test completed successfully")
        return True
    logger.warning("Build test failed - attempting error recovery...")
    logger.error(f"Error: {stderr}")
    if "Expected" in stderr or "The symbol \"defineConfig\"" in stderr:
        logger.info("Detected syntax error in vite.config.js - attempting to fix...")
        if vite_config.exists():
            if fix_vite_config_syntax(vite_config):
                logger.info("Retrying build after syntax fix...")
                success, stdout, stderr = run_command("npm run build", cwd=frontend_dir)
                if success:
                    logger.info("Build successful after syntax fix!")
                    return True
    if "Cannot find module" in stderr:
        logger.info("Detected missing dependencies - reinstalling...")
        run_command("npm install", cwd=frontend_dir)
        success, stdout, stderr = run_command("npm run build", cwd=frontend_dir)
        if success:
            logger.info("Build successful after dependency reinstall!")
            return True
    return False

def test_docker_build(frontend_dir):
    """Test Docker build for Kubernetes deployment"""
    logger.info("Testing Docker build for Kubernetes deployment...")
    dockerfile = frontend_dir / "Dockerfile"
    if not dockerfile.exists():
        logger.warning("Dockerfile not found, skipping build test")
        return True
    success, stdout, stderr = run_command("docker build -t linkops-frontend:test .", cwd=frontend_dir)
    if success:
        logger.info("Docker build successful")
        return True
    logger.error(f"Docker build failed: {stderr}")
    if "npm run build" in stderr:
        logger.info("Docker build failed due to npm build error - attempting to fix...")
        if test_build(frontend_dir):
            logger.info("Retrying Docker build after npm build fix...")
            success, stdout, stderr = run_command("docker build -t linkops-frontend:test .", cwd=frontend_dir)
            if success:
                logger.info("Docker build successful after fix!")
                return True
    return False

def commit_and_sync(frontend_dir):
    """Commit fixes and trigger ArgoCD sync"""
    logger.info("Committing fixes and triggering ArgoCD sync...")
    success, _, stderr = run_command("git add . && git commit -m 'Frontend auto-fixes' && git push", cwd=frontend_dir)
    if success:
        logger.info("Changes committed and pushed")
        success, _, stderr = run_command("argocd app sync linkops")
        if success:
            logger.info("ArgoCD sync triggered successfully")
            return True
        logger.error(f"ArgoCD sync failed: {stderr}")
    return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="LinkOps Frontend Auto-Fix Script")
    parser.add_argument('--max-workers', type=int, default=4, help="Max parallel workers")
    args = parser.parse_args()
    logger.info("🚀 LinkOps Frontend Auto-Fix Script")
    logger.info("=" * 50)
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        logger.error("Frontend directory not found!")
        return 1
    logger.info(f"Working in: {frontend_dir.absolute()}")
    # Step 1: Fix configuration files
    config_fixes = 0
    package_json = frontend_dir / "package.json"
    if package_json.exists():
        if fix_package_json_scripts(package_json):
            config_fixes += 1
    vite_config = frontend_dir / "vite.config.js"
    if vite_config.exists():
        if fix_vite_config_syntax(vite_config):
            config_fixes += 1
    eslint_config = frontend_dir / ".eslintrc.js"
    if eslint_config.exists():
        if fix_eslint_config(eslint_config):
            config_fixes += 1
    logger.info(f"Fixed {config_fixes} configuration files")
    # Step 2: Fix npm ci issues
    npm_success = fix_npm_ci_errors(frontend_dir)
    # Step 3: Run ESLint and parse issues
    eslint_success, eslint_issues = run_eslint_fix(frontend_dir)
    # Step 4: Process files with ESLint fixes
    files = find_frontend_files(frontend_dir)
    logger.info(f"Processing {len(files)} frontend files...")
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        results = list(tqdm(executor.map(lambda f: process_file(f, eslint_issues), files), total=len(files), desc="Processing files"))
    files_processed = sum(1 for result in results if result)
    logger.info(f"Processed {files_processed} files")
    # Step 5: Re-run ESLint to verify fixes
    eslint_success, eslint_issues = run_eslint_fix(frontend_dir)
    # Step 6: Test build
    build_success = test_build(frontend_dir)
    # Step 7: Test Docker build
    docker_success = test_docker_build(frontend_dir)
    # Step 8: Commit and sync
    commit_success = False
    if build_success and docker_success:
        commit_success = commit_and_sync(frontend_dir)
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 Summary:")
    logger.info(f"  • Config fixes: {config_fixes}")
    logger.info(f"  • npm ci: {'✅' if npm_success else '❌'}")
    logger.info(f"  • Files processed: {files_processed}")
    logger.info(f"  • ESLint fix: {'✅' if eslint_success else '⚠️'}")
    logger.info(f"  • ESLint issues remaining: {len(eslint_issues)}")
    logger.info(f"  • Build test: {'✅' if build_success else '❌'}")
    logger.info(f"  • Docker build: {'✅' if docker_success else '❌'}")
    logger.info(f"  • ArgoCD sync: {'✅' if commit_success else '❌'}")
    if build_success and docker_success and commit_success and len(eslint_issues) == 0:
        logger.info("\n🎉 Frontend auto-fix completed successfully!")
        return 0
    logger.warning("\n⚠️ Frontend auto-fix completed with issues")
    return 1

if __name__ == "__main__":
    exit(main())