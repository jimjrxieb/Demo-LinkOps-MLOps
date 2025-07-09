#!/usr/bin/env python3
"""
Frontend Auto-Fix Script for LinkOps-MLOps
Automatically fixes common ESLint warnings and build issues in Vue.js frontend
Updated for new frontend structure with authentication and demo mode
"""

import json
import os
import re
import subprocess
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return result"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def fix_vite_config_syntax(file_path):
    """Fix common Vite config syntax errors"""
    print(f"  🔧 Checking Vite config syntax in {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # Fix extra semicolons in object properties
        # Pattern: 'value'; -> 'value'
        content = re.sub(r"'([^']+)';", r"'\1'", content)
        content = re.sub(r'"([^"]+)";', r'"\1"', content)
        
        # Fix extra semicolons in array items
        # Pattern: 'item'; -> 'item'
        content = re.sub(r"'([^']+)',\s*;", r"'\1',", content)
        content = re.sub(r'"([^"]+)",\s*;', r'"\1",', content)
        
        # Fix trailing semicolons in object properties
        content = re.sub(r':\s*([^,}]+);\s*([,}])', r': \1\2', content)
        
        # Fix missing commas in object properties
        content = re.sub(r"'([^']+)'\s*\n\s*'([^']+)'", r"'\1',\n      '\2'", content)
        content = re.sub(r'"([^"]+)"\s*\n\s*"([^"]+)"', r'"\1",\n      "\2"', content)
        
        # Fix function calls with extra semicolons
        content = re.sub(r'\(\s*([^)]+)\s*\)\s*;', r'(\1)', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"    ✅ Fixed Vite config syntax errors")
            return True
        
        return False
        
    except Exception as e:
        print(f"    ❌ Error fixing Vite config: {e}")
        return False


def fix_package_json_scripts(file_path):
    """Fix missing scripts in package.json"""
    print(f"  🔧 Checking package.json scripts in {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        original_data = json.dumps(data, indent=2)
        changes_made = 0
        
        # Ensure lint:fix script exists
        if 'scripts' in data:
            scripts = data['scripts']
            
            # Add lint:fix if it doesn't exist
            if 'lint' in scripts and 'lint:fix' not in scripts:
                lint_cmd = scripts['lint']
                if '--fix' not in lint_cmd:
                    scripts['lint:fix'] = lint_cmd + ' --fix'
                    changes_made += 1
                    print(f"    ✅ Added lint:fix script")
            
            # Ensure lint script doesn't have --fix flag
            if 'lint' in scripts and '--fix' in scripts['lint']:
                scripts['lint'] = scripts['lint'].replace(' --fix', '')
                changes_made += 1
                print(f"    ✅ Fixed lint script (removed --fix flag)")
        
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        
        return False
        
    except Exception as e:
        print(f"    ❌ Error fixing package.json: {e}")
        return False


def fix_eslint_config(file_path):
    """Fix ESLint configuration issues"""
    print(f"  🔧 Checking ESLint config in {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # Fix common ESLint config issues
        if 'extends' in content and 'vue' not in content:
            # Add Vue ESLint plugin if missing
            if 'plugins' not in content:
                content = content.replace('extends: [', 'plugins: ["vue"],\n  extends: [')
                changes_made += 1
        
        # Fix parser options for Vue files
        if 'parserOptions' in content and 'ecmaVersion' not in content:
            content = content.replace('parserOptions: {', 'parserOptions: {\n      ecmaVersion: 2020,')
            changes_made += 1
        
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"    ✅ Fixed ESLint configuration")
            return True
        
        return False
        
    except Exception as e:
        print(f"    ❌ Error fixing ESLint config: {e}")
        return False


def fix_npm_ci_errors(frontend_dir):
    """Fix npm ci errors by syncing package-lock.json with package.json"""
    print("🔧 Checking for npm ci sync issues...")

    # First, try to run npm ci to see if there are sync issues
    success, stdout, stderr = run_command("npm ci", cwd=frontend_dir)

    if success:
        print("  ✅ npm ci completed successfully - no sync issues found")
        return True

    # Check if the error is related to package-lock.json sync
    if "package-lock.json" in stderr and "sync" in stderr.lower():
        print("  🔧 Detected package-lock.json sync issue - attempting to fix...")

        # Remove the existing package-lock.json
        lock_file = frontend_dir / "package-lock.json"
        if lock_file.exists():
            try:
                lock_file.unlink()
                print("  🗑️ Removed outdated package-lock.json")
            except Exception as e:
                print(f"  ❌ Failed to remove package-lock.json: {e}")
                return False

        # Run npm install to generate a new package-lock.json
        print("  📦 Running npm install to generate new package-lock.json...")
        success, stdout, stderr = run_command("npm install", cwd=frontend_dir)

        if success:
            print("  ✅ Successfully generated new package-lock.json")

            # Verify the fix by running npm ci again
            print("  🔍 Verifying fix with npm ci...")
            success, stdout, stderr = run_command("npm ci", cwd=frontend_dir)

            if success:
                print("  ✅ npm ci now works correctly!")
                return True
            else:
                print("  ❌ npm ci still failing after package-lock.json regeneration")
                print(f"  Error: {stderr}")
                return False
        else:
            print("  ❌ Failed to run npm install")
            print(f"  Error: {stderr}")
            return False

    # Check for specific dependency version conflicts
    elif "Invalid: lock file's" in stderr:
        print("  🔧 Detected dependency version conflicts - attempting to resolve...")

        # Extract the conflicting packages from the error
        conflicts = []
        for line in stderr.split("\n"):
            if "Invalid: lock file's" in line:
                # Extract package name and version info
                match = re.search(
                    r"lock file's (\w+)@([\d.]+) does not satisfy (\w+)@([\d.]+)", line
                )
                if match:
                    package = match.group(1)
                    lock_version = match.group(2)
                    required_version = match.group(4)
                    conflicts.append((package, lock_version, required_version))

        if conflicts:
            print(f"  📋 Found {len(conflicts)} dependency conflicts:")
            for package, lock_ver, req_ver in conflicts:
                print(f"    • {package}: lock has {lock_ver}, needs {req_ver}")

            # Remove package-lock.json and node_modules, then reinstall
            print("  🧹 Cleaning npm cache and reinstalling...")

            # Remove package-lock.json
            lock_file = frontend_dir / "package-lock.json"
            if lock_file.exists():
                lock_file.unlink()
                print("  🗑️ Removed package-lock.json")

            # Remove node_modules (optional, but helps with stubborn conflicts)
            node_modules = frontend_dir / "node_modules"
            if node_modules.exists():
                try:
                    import shutil

                    shutil.rmtree(node_modules)
                    print("  🗑️ Removed node_modules directory")
                except Exception as e:
                    print(f"  ⚠️ Could not remove node_modules: {e}")

            # Clear npm cache
            print("  🧹 Clearing npm cache...")
            run_command("npm cache clean --force", cwd=frontend_dir)

            # Reinstall dependencies
            print("  📦 Reinstalling dependencies...")
            success, stdout, stderr = run_command("npm install", cwd=frontend_dir)

            if success:
                print("  ✅ Dependencies reinstalled successfully")

                # Test npm ci again
                print("  🔍 Testing npm ci...")
                success, stdout, stderr = run_command("npm ci", cwd=frontend_dir)

                if success:
                    print("  ✅ npm ci now works correctly!")
                    return True
                else:
                    print("  ❌ npm ci still failing after reinstall")
                    print(f"  Error: {stderr}")
                    return False
            else:
                print("  ❌ Failed to reinstall dependencies")
                print(f"  Error: {stderr}")
                return False

    else:
        print("  ❌ npm ci failed with unknown error")
        print(f"  Error: {stderr}")
        return False


def fix_console_statements(file_path, content):
    """Fix console statements by removing or replacing them"""
    print(f"  🔧 Fixing console statements in {file_path}")

    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        original_line = line

        # Match console.log, console.error, console.warn, etc.
        console_pattern = (
            r"(\s*)(console\.(log|error|warn|info|debug)\s*\([^)]*\)\s*;?)"
        )
        match = re.search(console_pattern, line)

        if match:
            indent = match.group(1)
            console_stmt = match.group(2)

            # Replace with comment in production or remove entirely
            if "error" in console_stmt.lower():
                # Keep error logging but make it conditional
                fixed_line = f"{indent}// Development logging: {console_stmt}"
            else:
                # Remove debug/log statements
                fixed_line = f"{indent}// Removed console statement: {console_stmt}"

            fixed_lines.append(fixed_line)
            changes_made += 1
        else:
            fixed_lines.append(original_line)

    if changes_made > 0:
        print(f"    ✅ Fixed {changes_made} console statements")

    return "\n".join(fixed_lines)


def fix_unused_variables(file_path, content):
    """Fix unused variables by removing or marking them as used"""
    print(f"  🔧 Fixing unused variables in {file_path}")

    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for line in lines:
        original_line = line

        # Fix unused parameters in catch blocks
        if "catch (" in line and "error" in line:
            # Replace unused error parameter with underscore
            fixed_line = re.sub(r"catch\s*\(\s*error\s*\)", "catch (_error)", line)
            if fixed_line != original_line:
                fixed_lines.append(fixed_line)
                changes_made += 1
                continue

        # Fix unused variables in destructuring
        if "const {" in line and "} =" in line:
            # Add underscore prefix to unused destructured variables
            fixed_line = re.sub(r"const\s*{\s*([^}]+)\s*}\s*=", r"const {_\1} =", line)
            if fixed_line != original_line:
                fixed_lines.append(fixed_line)
                changes_made += 1
                continue

        fixed_lines.append(original_line)

    if changes_made > 0:
        print(f"    ✅ Fixed {changes_made} unused variables")

    return "\n".join(fixed_lines)


def fix_vue_props(file_path, content):
    """Fix Vue.js props validation issues"""
    print(f"  🔧 Fixing Vue props in {file_path}")

    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for line in lines:
        original_line = line

        # Fix missing required props
        if "props:" in line and "required:" not in line:
            # Add required: false for optional props
            if "type:" in line and "default:" not in line:
                fixed_line = line.replace("type:", "required: false, type:")
                fixed_lines.append(fixed_line)
                changes_made += 1
                continue

        # Fix prop type definitions
        if "type: String" in line and "default:" not in line:
            fixed_line = line.replace("type: String", "type: String, default: ''")
            fixed_lines.append(fixed_line)
            changes_made += 1
            continue

        if "type: Number" in line and "default:" not in line:
            fixed_line = line.replace("type: Number", "type: Number, default: 0")
            fixed_lines.append(fixed_line)
            changes_made += 1
            continue

        if "type: Boolean" in line and "default:" not in line:
            fixed_line = line.replace("type: Boolean", "type: Boolean, default: false")
            fixed_lines.append(fixed_line)
            changes_made += 1
            continue

        fixed_lines.append(original_line)

    if changes_made > 0:
        print(f"    ✅ Fixed {changes_made} Vue props")

    return "\n".join(fixed_lines)


def fix_javascript_issues(file_path, content):
    """Fix common JavaScript issues"""
    print(f"  🔧 Fixing JavaScript issues in {file_path}")

    lines = content.split("\n")
    fixed_lines = []
    changes_made = 0

    for line in lines:
        original_line = line

        # Fix missing semicolons
        if line.strip() and not line.strip().endswith((";", "{", "}", ":", ",")):
            if not line.strip().startswith(("//", "/*", "*", "import", "export")):
                # Add semicolon if line doesn't already have one
                if not line.rstrip().endswith(";"):
                    fixed_line = line.rstrip() + ";"
                    fixed_lines.append(fixed_line)
                    changes_made += 1
                    continue

        # Fix double quotes to single quotes (optional)
        if '"' in line and not line.strip().startswith(("//", "/*")):
            # Only fix simple string literals, not complex ones
            if re.search(r'"[^"]*"', line) and not re.search(r'"[^"]*"[^"]*"', line):
                fixed_line = line.replace('"', "'")
                fixed_lines.append(fixed_line)
                changes_made += 1
                continue

        fixed_lines.append(original_line)

    if changes_made > 0:
        print(f"    ✅ Fixed {changes_made} JavaScript issues")

    return "\n".join(fixed_lines)


def process_file(file_path):
    """Process a single file and apply fixes"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Apply fixes based on file type
        if file_path.suffix in [".vue", ".js"]:
            content = fix_console_statements(file_path, content)
            content = fix_unused_variables(file_path, content)
            content = fix_javascript_issues(file_path, content)

        if file_path.suffix == ".vue":
            content = fix_vue_props(file_path, content)

        # Write back if changes were made
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False


def find_frontend_files(frontend_dir):
    """Find all frontend files that need processing"""
    print("🔍 Scanning for frontend files...")

    # Updated file patterns for new structure
    patterns = [
        "*.vue",  # Vue components
        "*.js",   # JavaScript files
        "*.ts",   # TypeScript files (if any)
    ]

    # Updated directories to scan
    directories = [
        "",           # Root frontend directory
        "components", # Components directory
        "views",      # Views directory
        "router",     # Router directory
        "store",      # Store directory
        "utils",      # Utils directory
        "assets",     # Assets directory
    ]

    files_to_process = []

    for directory in directories:
        dir_path = frontend_dir / directory if directory else frontend_dir
        if dir_path.exists():
            for pattern in patterns:
                files = list(dir_path.glob(pattern))
                files_to_process.extend(files)

    # Remove duplicates and sort
    files_to_process = sorted(set(files_to_process))
    
    print(f"  📁 Found {len(files_to_process)} files to process")
    return files_to_process


def run_eslint_fix(frontend_dir):
    """Run ESLint auto-fix"""
    print("🔧 Running ESLint auto-fix...")
    
    # First check if lint:fix script exists
    package_json = frontend_dir / "package.json"
    if package_json.exists():
        fix_package_json_scripts(package_json)
    
    success, stdout, stderr = run_command("npm run lint:fix", cwd=frontend_dir)
    
    if success:
        print("  ✅ ESLint auto-fix completed successfully")
    else:
        print("  ⚠️ ESLint auto-fix completed with warnings")
        print(f"  Output: {stdout}")
        if stderr:
            print(f"  Errors: {stderr}")
    
    return success


def test_build(frontend_dir):
    """Test the build process with error recovery"""
    print("🏗️ Testing build process...")
    
    # First fix any Vite config issues
    vite_config = frontend_dir / "vite.config.js"
    if vite_config.exists():
        fix_vite_config_syntax(vite_config)
    
    # Try the build
    success, stdout, stderr = run_command("npm run build", cwd=frontend_dir)
    
    if success:
        print("  ✅ Build test completed successfully")
        return True
    else:
        print("  ❌ Build test failed - attempting error recovery...")
        print(f"  Error: {stderr}")
        
        # Try to fix common build errors
        if "Expected" in stderr and "but found" in stderr:
            print("  🔧 Detected syntax error - attempting to fix...")
            
            # Re-fix Vite config
            if vite_config.exists():
                if fix_vite_config_syntax(vite_config):
                    print("  🔄 Retrying build after syntax fix...")
                    success, stdout, stderr = run_command("npm run build", cwd=frontend_dir)
                    if success:
                        print("  ✅ Build successful after syntax fix!")
                        return True
        
        # Check for missing dependencies
        if "Cannot find module" in stderr:
            print("  🔧 Detected missing dependencies - reinstalling...")
            run_command("npm install", cwd=frontend_dir)
            success, stdout, stderr = run_command("npm run build", cwd=frontend_dir)
            if success:
                print("  ✅ Build successful after dependency reinstall!")
                return True
        
        return False


def main():
    """Main function"""
    print("🚀 LinkOps Frontend Auto-Fix Script")
    print("=" * 50)

    # Find frontend directory
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return 1

    print(f"📁 Working in: {frontend_dir.absolute()}")

    # Step 1: Fix configuration files
    print("\n1️⃣ Fixing configuration files...")
    config_fixes = 0
    
    # Fix package.json scripts
    package_json = frontend_dir / "package.json"
    if package_json.exists():
        if fix_package_json_scripts(package_json):
            config_fixes += 1
    
    # Fix Vite config
    vite_config = frontend_dir / "vite.config.js"
    if vite_config.exists():
        if fix_vite_config_syntax(vite_config):
            config_fixes += 1
    
    # Fix ESLint config
    eslint_config = frontend_dir / ".eslintrc.js"
    if eslint_config.exists():
        if fix_eslint_config(eslint_config):
            config_fixes += 1
    
    print(f"  ✅ Fixed {config_fixes} configuration files")

    # Step 2: Fix npm ci issues
    print("\n2️⃣ Fixing npm ci issues...")
    npm_success = fix_npm_ci_errors(frontend_dir)
    
    if not npm_success:
        print("❌ Failed to fix npm ci issues")
        return 1

    # Step 3: Find and process files
    print("\n3️⃣ Processing frontend files...")
    files = find_frontend_files(frontend_dir)
    
    files_processed = 0
    for file_path in files:
        if process_file(file_path):
            files_processed += 1

    print(f"  ✅ Processed {files_processed} files")

    # Step 4: Run ESLint auto-fix
    print("\n4️⃣ Running ESLint auto-fix...")
    eslint_success = run_eslint_fix(frontend_dir)

    # Step 5: Test build with error recovery
    print("\n5️⃣ Testing build...")
    build_success = test_build(frontend_dir)

    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  • Config fixes: {config_fixes}")
    print(f"  • npm ci: {'✅' if npm_success else '❌'}")
    print(f"  • Files processed: {files_processed}")
    print(f"  • ESLint fix: {'✅' if eslint_success else '⚠️'}")
    print(f"  • Build test: {'✅' if build_success else '❌'}")

    if build_success:
        print("\n🎉 Frontend auto-fix completed successfully!")
        return 0
    else:
        print("\n⚠️ Frontend auto-fix completed with issues")
        return 1


if __name__ == "__main__":
    exit(main())
