#!/usr/bin/env python3
"""
Comprehensive lint and formatting fix script for DEMO-LinkOps.

This script performs the following operations in order:
1. Auto-fixes import sorting with isort
2. Auto-fixes code formatting with black
3. Auto-fixes ruff violations where possible
4. Reports remaining issues that need manual intervention

The order is designed to prevent tool conflicts.
"""

import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class LintFixer:
    """Comprehensive code quality fixer for the DEMO-LinkOps project."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.python_dirs = [
            "unified-api",
            "ml-models",
            "pipeline",
            "rag",
            "sync_engine",
        ]

    def run_command(self, cmd: List[str], description: str) -> Tuple[bool, str, str]:
        """Run a command and return success status, stdout, stderr."""
        try:
            logger.info(f"🔧 {description}...")
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            success = result.returncode == 0
            if success:
                logger.info(f"✅ {description} completed successfully")
            else:
                logger.warning(f"⚠️  {description} completed with warnings/errors")

            return success, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            logger.error(f"❌ {description} timed out")
            return False, "", "Command timed out"
        except Exception as e:
            logger.error(f"❌ {description} failed: {e}")
            return False, "", str(e)

    def fix_imports(self) -> bool:
        """Fix import ordering with isort."""
        success, stdout, stderr = self.run_command(
            ["python3", "-m", "isort", ".", "--profile", "black"],
            "Fixing import ordering with isort",
        )

        if not success:
            logger.warning(f"isort warnings/errors:\n{stderr}")

        return success

    def format_code(self) -> bool:
        """Format code with black."""
        success, stdout, stderr = self.run_command(
            ["python3", "-m", "black", ".", "--line-length", "88"],
            "Formatting code with black",
        )

        if not success:
            logger.warning(f"black warnings/errors:\n{stderr}")

        return success

    def fix_ruff_issues(self) -> bool:
        """Fix auto-fixable ruff issues."""
        success, stdout, stderr = self.run_command(
            ["python3", "-m", "ruff", "check", ".", "--fix"], "Fixing ruff violations"
        )

        if not success:
            logger.warning(f"ruff warnings/errors:\n{stderr}")

        return success

    def check_remaining_issues(self) -> Dict[str, List[str]]:
        """Check for remaining issues after fixes."""
        issues = {}

        # Check ruff
        success, stdout, stderr = self.run_command(
            ["python3", "-m", "ruff", "check", "."], "Checking remaining ruff issues"
        )
        if not success:
            issues["ruff"] = stderr.split("\n") if stderr else []

        # Check mypy for type issues (optional)
        try:
            success, stdout, stderr = self.run_command(
                ["python3", "-m", "mypy", ".", "--ignore-missing-imports"],
                "Checking type issues with mypy",
            )
            if not success:
                issues["mypy"] = stderr.split("\n") if stderr else []
        except Exception:
            logger.info("mypy not available, skipping type checks")

        return issues

    def fix_common_issues(self) -> bool:
        """Fix common Python issues programmatically."""
        logger.info("🔧 Fixing common code issues...")

        fixed_files = []

        # Find all Python files
        for py_file in self.project_root.rglob("*.py"):
            if any(
                exclude in str(py_file)
                for exclude in [".git", "__pycache__", ".venv", "venv"]
            ):
                continue

            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                original_content = content

                # Fix common issues
                content = self._fix_file_content(content)

                if content != original_content:
                    with open(py_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    fixed_files.append(str(py_file))

            except Exception as e:
                logger.warning(f"Could not process {py_file}: {e}")

        if fixed_files:
            logger.info(f"✅ Fixed common issues in {len(fixed_files)} files")
            for file_path in fixed_files[:10]:  # Show first 10
                logger.info(f"   - {file_path}")
            if len(fixed_files) > 10:
                logger.info(f"   - ... and {len(fixed_files) - 10} more files")
        else:
            logger.info("✅ No common issues found to fix")

        return len(fixed_files) > 0

    def _fix_file_content(self, content: str) -> str:
        """Fix common issues in file content."""
        lines = content.split("\n")
        fixed_lines = []

        for line in lines:
            # Fix bare except clauses
            if "except:" in line and "except Exception:" not in line:
                line = line.replace("except:", "except Exception:")

            # Fix unused imports (simple cases)
            if line.strip().startswith("import ") and " as " not in line:
                # This is a simple heuristic - more complex cases need manual review
                pass

            fixed_lines.append(line)

        return "\n".join(fixed_lines)

    def run_all_fixes(self) -> bool:
        """Run all fixes in the correct order."""
        logger.info("🚀 Starting comprehensive code quality fixes...")

        steps = [
            ("Fix common issues", self.fix_common_issues),
            ("Fix imports", self.fix_imports),
            ("Format code", self.format_code),
            ("Fix ruff issues", self.fix_ruff_issues),
        ]

        all_success = True
        for step_name, step_func in steps:
            try:
                success = step_func()
                if not success:
                    logger.warning(f"⚠️  {step_name} had some issues but continued")
                    all_success = False
            except Exception as e:
                logger.error(f"❌ {step_name} failed: {e}")
                all_success = False

        # Check remaining issues
        remaining_issues = self.check_remaining_issues()
        if remaining_issues:
            logger.warning("⚠️  Some issues remain that need manual attention:")
            for tool, issues in remaining_issues.items():
                if issues:
                    logger.warning(f"  {tool}: {len(issues)} issues")
                    # Show first few issues
                    for issue in issues[:3]:
                        if issue.strip():
                            logger.warning(f"    - {issue.strip()}")
                    if len(issues) > 3:
                        logger.warning(f"    - ... and {len(issues) - 3} more")
        else:
            logger.info("🎉 All automated fixes completed successfully!")

        return all_success and not remaining_issues


def main():
    """Main entry point."""
    project_root = Path(__file__).parent

    # Check if required tools are installed
    required_tools = ["black", "isort", "ruff"]
    missing_tools = []

    for tool in required_tools:
        try:
            subprocess.run(
                ["python3", "-m", tool, "--version"], capture_output=True, check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(tool)

    if missing_tools:
        logger.error(f"❌ Missing required tools: {', '.join(missing_tools)}")
        logger.info("Install them with: pip install black isort ruff")
        return False

    # Run fixes
    fixer = LintFixer(project_root)
    success = fixer.run_all_fixes()

    if success:
        logger.info("🎉 All fixes completed successfully!")
        return True
    else:
        logger.warning("⚠️  Some issues remain - check the output above")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
