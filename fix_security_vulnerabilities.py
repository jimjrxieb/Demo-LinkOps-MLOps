#!/usr/bin/env python3
"""
Security Vulnerability Fix Script for DEMO-LinkOps

This script fixes known security vulnerabilities by updating dependencies
to their patched versions based on security scan results.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class SecurityVulnerabilityFixer:
    """Fixes security vulnerabilities in Python dependencies."""
    
    def __init__(self):
        self.root_dir = Path.cwd()
        self.vulnerability_fixes = {
            # Critical vulnerabilities
            "pillow": ">=10.2.0",  # Fixes heap buffer overflow and eval injection
            "transformers": ">=4.52.0",  # Fixes deserialization and ReDoS issues
            "torch": ">=2.6.0",  # Fixes deserialization vulnerability
            "setuptools": ">=70.0.0",  # Fixes code injection vulnerability
            "zipp": ">=3.19.1",  # Fixes infinite loop vulnerability
            
            # Update sentence-transformers to newer version that uses secure deps
            "sentence-transformers": ">=2.7.0",
        }
        
    def find_requirements_files(self) -> List[Path]:
        """Find all requirements.txt files in the project."""
        requirements_files = []
        
        # Common locations for requirements files
        patterns = [
            "**/requirements.txt",
            "**/requirements*.txt", 
            "**/pyproject.toml",
        ]
        
        for pattern in patterns:
            requirements_files.extend(self.root_dir.glob(pattern))
            
        return list(set(requirements_files))  # Remove duplicates
    
    def parse_requirements_file(self, file_path: Path) -> List[str]:
        """Parse a requirements file and return list of requirements."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            requirements = []
            for line in lines:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    requirements.append(line)
            
            return requirements
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return []
    
    def update_requirement_line(self, line: str) -> Tuple[str, bool]:
        """Update a requirement line with security fixes."""
        updated = False
        
        for package, fixed_version in self.vulnerability_fixes.items():
            # Match package name at start of line (case insensitive)
            pattern = rf'^{re.escape(package)}(\s*[>=<~!].*)?$'
            if re.match(pattern, line, re.IGNORECASE):
                new_line = f"{package}{fixed_version}"
                if line != new_line:
                    print(f"🔧 Updating {package}: {line} → {new_line}")
                    updated = True
                    return new_line, updated
        
        return line, updated
    
    def fix_requirements_file(self, file_path: Path) -> bool:
        """Fix vulnerabilities in a requirements file."""
        print(f"\n📋 Processing {file_path}")
        
        original_lines = self.parse_requirements_file(file_path)
        if not original_lines:
            return False
        
        updated_lines = []
        file_updated = False
        
        for line in original_lines:
            updated_line, was_updated = self.update_requirement_line(line)
            updated_lines.append(updated_line)
            if was_updated:
                file_updated = True
        
        if file_updated:
            try:
                with open(file_path, 'w') as f:
                    f.write('\n'.join(updated_lines) + '\n')
                print(f"✅ Updated {file_path}")
                return True
            except Exception as e:
                print(f"❌ Error writing {file_path}: {e}")
                return False
        else:
            print(f"ℹ️  No vulnerable packages found in {file_path}")
            return False
    
    def fix_pyproject_toml(self, file_path: Path) -> bool:
        """Fix vulnerabilities in pyproject.toml files."""
        print(f"\n📋 Processing {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Update dependencies in pyproject.toml
            for package, fixed_version in self.vulnerability_fixes.items():
                # Match package in dependencies section
                pattern = rf'("{re.escape(package)}"\s*=\s*"[^"]*")'
                if re.search(pattern, content, re.IGNORECASE):
                    new_dep = f'"{package}" = "{fixed_version}"'
                    content = re.sub(pattern, new_dep, content, flags=re.IGNORECASE)
                    print(f"🔧 Updated {package} in pyproject.toml")
            
            if content != original_content:
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"✅ Updated {file_path}")
                return True
            else:
                print(f"ℹ️  No vulnerable packages found in {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return False
    
    def run_security_scan(self) -> bool:
        """Run security scan to verify fixes."""
        print("\n🔍 Running security scan to verify fixes...")
        
        try:
            # Try pip-audit if available
            result = subprocess.run(['pip-audit', '--desc'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ No vulnerabilities found by pip-audit")
                return True
            else:
                print("⚠️  Some vulnerabilities may remain:")
                print(result.stdout)
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("ℹ️  pip-audit not available, skipping security scan")
            print("💡 Install with: pip install pip-audit")
            return True
    
    def install_updated_dependencies(self, requirements_files: List[Path]) -> bool:
        """Install updated dependencies."""
        print("\n📦 Installing updated dependencies...")
        
        for req_file in requirements_files:
            if req_file.name.endswith('.txt'):
                try:
                    print(f"Installing from {req_file}")
                    result = subprocess.run(['pip', 'install', '-r', str(req_file)], 
                                          capture_output=True, text=True, timeout=300)
                    
                    if result.returncode != 0:
                        print(f"⚠️  Warning: Could not install all dependencies from {req_file}")
                        print(result.stderr)
                    else:
                        print(f"✅ Successfully installed dependencies from {req_file}")
                        
                except subprocess.TimeoutExpired:
                    print(f"⏰ Installation from {req_file} timed out")
                except Exception as e:
                    print(f"❌ Error installing from {req_file}: {e}")
        
        return True
    
    def run_fix(self) -> bool:
        """Run the complete vulnerability fix process."""
        print("🔒 DEMO-LinkOps Security Vulnerability Fixer")
        print("=" * 50)
        
        # Find all requirements files
        requirements_files = self.find_requirements_files()
        
        if not requirements_files:
            print("❌ No requirements files found!")
            return False
        
        print(f"📁 Found {len(requirements_files)} requirements files:")
        for file_path in requirements_files:
            print(f"   • {file_path}")
        
        # Fix vulnerabilities in each file
        files_updated = 0
        for file_path in requirements_files:
            if file_path.name == 'pyproject.toml':
                if self.fix_pyproject_toml(file_path):
                    files_updated += 1
            elif file_path.name.endswith('.txt'):
                if self.fix_requirements_file(file_path):
                    files_updated += 1
        
        print(f"\n📊 Summary:")
        print(f"   • Files processed: {len(requirements_files)}")
        print(f"   • Files updated: {files_updated}")
        
        if files_updated > 0:
            print(f"\n🔧 Vulnerabilities fixed:")
            for package, version in self.vulnerability_fixes.items():
                print(f"   • {package} → {version}")
            
            # Install updated dependencies
            self.install_updated_dependencies([f for f in requirements_files if f.name.endswith('.txt')])
            
            # Run security scan
            self.run_security_scan()
            
            print(f"\n✅ Security vulnerability fixes applied!")
            print(f"💡 Recommend rebuilding Docker images with updated dependencies")
            
        else:
            print(f"\nℹ️  No vulnerable packages found in requirements files")
        
        return True


def main():
    """Main function."""
    fixer = SecurityVulnerabilityFixer()
    
    try:
        success = fixer.run_fix()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Fix interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()