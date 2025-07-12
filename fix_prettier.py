def sanitize_cmd(cmd):
    import shlex
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {"ls", "echo", "kubectl", "helm", "python3", "cat", "go", "docker", "npm", "black", "ruff", "yamllint", "prettier", "flake8"}
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd
#!/usr/bin/env python3
"""
Script to fix Prettier formatting issues in Vue files.
"""

import os
import subprocess  # nosec B404
import sys


def run_prettier_fix():
    """Run Prettier to fix formatting issues."""
    try:
        # Change to frontend directory
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        if not os.path.exists(frontend_dir):
            print("❌ Frontend directory not found")
            return False

        os.chdir(frontend_dir)
        print(f"📁 Working in: {os.getcwd()}")

        # Check if node_modules exists
        if not os.path.exists("node_modules"):
            print("📦 Installing dependencies...")
            subprocess.run(sanitize_cmd(["npm", "install"]), check=True)

        # Run Prettier to fix formatting
        print("🎨 Running Prettier to fix formatting...")
        result = subprocess.run(
            sanitize_cmd([
                "npx",
                "prettier",
                "--write",
                "src/components/DemoBanner.vue",
                "src/components/JamesGUI.vue",
            ]),
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ Prettier formatting fixed successfully!")
            if result.stdout:
                print("📝 Output:", result.stdout)
            return True
        else:
            print("❌ Prettier failed:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def verify_fixes():
    """Verify that Prettier issues are resolved."""
    try:
        os.chdir("frontend")

        print("🔍 Verifying fixes...")
        result = subprocess.run(
            sanitize_cmd([
                "npx",
                "prettier",
                "--check",
                "src/components/DemoBanner.vue",
                "src/components/JamesGUI.vue",
            ]),
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ All Prettier issues resolved!")
            return True
        else:
            print("❌ Prettier issues still exist:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False


def main():
    """Main function."""
    print("🚀 Starting Prettier formatting fixes...")

    # Fix formatting
    if run_prettier_fix():
        # Verify fixes
        if verify_fixes():
            print("\n🎉 All Prettier formatting issues have been resolved!")
            return True
        else:
            print("\n⚠️ Some issues may still exist")
            return False
    else:
        print("\n❌ Failed to fix Prettier issues")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
