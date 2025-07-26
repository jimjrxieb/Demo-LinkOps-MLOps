#!/usr/bin/env python3
"""
Automated fix script for common linting errors in DEMO-LinkOps.

This script fixes common Python linting issues that can be automatically resolved.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List


class LintFixer:
    """Automatic linting error fixer for Python code."""

    def __init__(self):
        self.root_dir = Path(".")
        self.python_dirs = [
            "unified-api",
            "rag",
            "ml-models", 
            "pipeline",
            "sync_engine",
            "htc",
            "scripts"
        ]

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project."""
        python_files = []
        
        for directory in self.python_dirs:
            dir_path = self.root_dir / directory
            if dir_path.exists():
                python_files.extend(dir_path.rglob("*.py"))
        
        # Also check root directory
        python_files.extend(self.root_dir.glob("*.py"))
        
        return python_files

    def fix_exception_chaining(self, file_path: Path) -> int:
        """Fix B904 errors: Add 'from err' to raise statements in except blocks."""
        fixes_count = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern to match raise HTTPException inside except blocks
            # This is a simplified fix - for production, use AST parsing
            patterns = [
                (
                    r'(\s+)except\s+Exception\s+as\s+(\w+):\s*\n(.*?)\n(\s+)raise\s+HTTPException\(',
                    r'\1except Exception as \2:\n\3\n\4raise HTTPException('
                ),
                (
                    r'(\s+)except\s+Exception\s+as\s+(\w+):\s*\n(.*?)\n(\s+)raise\s+ValueError\(',
                    r'\1except Exception as \2:\n\3\n\4raise ValueError('
                )
            ]
            
            # Simple fix: add "from e" to raise statements in except blocks
            lines = content.split('\n')
            in_except_block = False
            except_var = None
            
            for i, line in enumerate(lines):
                # Check if we're entering an except block
                except_match = re.match(r'(\s*)except\s+Exception\s+as\s+(\w+):', line)
                if except_match:
                    in_except_block = True
                    except_var = except_match.group(2)
                    continue
                
                # Check if we're leaving the except block (dedent)
                if in_except_block and line.strip() and not line.startswith(' '):
                    in_except_block = False
                    except_var = None
                
                # Fix raise statements in except blocks
                if in_except_block and except_var and 'raise ' in line and ' from ' not in line:
                    if 'HTTPException(' in line or 'ValueError(' in line:
                        # Add "from {except_var}" before the closing of the statement
                        if line.rstrip().endswith(')'):
                            lines[i] = line.rstrip()[:-1] + f') from {except_var}'
                            fixes_count += 1
                        elif i + 1 < len(lines) and ')' in lines[i + 1]:
                            # Multi-line statement
                            lines[i + 1] = lines[i + 1].replace(')', f') from {except_var}', 1)
                            fixes_count += 1
            
            new_content = '\n'.join(lines)
            
            if new_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Fixed {fixes_count} exception chaining issues in {file_path}")
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
        
        return fixes_count

    def fix_unused_imports(self, file_path: Path) -> int:
        """Remove unused imports using autoflake."""
        try:
            result = subprocess.run([
                'python', '-m', 'autoflake',
                '--remove-all-unused-imports',
                '--in-place',
                str(file_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Cleaned unused imports in {file_path}")
                return 1
            else:
                print(f"⚠️  Could not clean imports in {file_path}: autoflake not available")
                return 0
        except FileNotFoundError:
            print("💡 Tip: Install autoflake for automatic unused import removal: pip install autoflake")
            return 0

    def run_ruff_unsafe_fixes(self):
        """Run ruff with unsafe fixes enabled."""
        try:
            dirs = [d for d in self.python_dirs if (self.root_dir / d).exists()]
            if dirs:
                subprocess.run([
                    'ruff', 'check', '--fix', '--unsafe-fixes'
                ] + dirs, check=False)
                print("✅ Applied unsafe ruff fixes")
        except FileNotFoundError:
            print("❌ Ruff not found. Install with: pip install ruff")

    def run(self):
        """Run all fixes."""
        print("🔧 DEMO-LinkOps Lint Error Fixer")
        print("=================================")
        
        python_files = self.find_python_files()
        
        if not python_files:
            print("❌ No Python files found!")
            return
        
        print(f"📁 Found {len(python_files)} Python files")
        
        total_fixes = 0
        
        # Fix exception chaining issues
        print("\n🔗 Fixing exception chaining issues...")
        for file_path in python_files:
            total_fixes += self.fix_exception_chaining(file_path)
        
        # Run ruff with unsafe fixes
        print("\n🛠️  Running ruff unsafe fixes...")
        self.run_ruff_unsafe_fixes()
        
        # Try to fix unused imports
        print("\n📦 Cleaning unused imports...")
        for file_path in python_files:
            total_fixes += self.fix_unused_imports(file_path)
        
        print(f"\n✅ Applied {total_fixes} automatic fixes!")
        print("\n💡 Next steps:")
        print("1. Run 'ruff check .' to see remaining issues")
        print("2. Run 'ruff format .' to format code")
        print("3. Review and fix remaining issues manually")


if __name__ == "__main__":
    fixer = LintFixer()
    fixer.run()