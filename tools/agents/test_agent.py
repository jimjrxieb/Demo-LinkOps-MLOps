def sanitize_cmd(cmd):
    import shlex

    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {
        "ls",
        "echo",
        "kubectl",
        "helm",
        "python3",
        "cat",
        "go",
        "docker",
        "npm",
        "black",
        "ruff",
        "yamllint",
        "prettier",
        "flake8",
    }
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd


#!/usr/bin/env python3
"""
Test script for the LinkOps Platform Agent
Tests both the Go agent directly and the API integration
"""

import json
import os
import subprocess  # nosec B404
import sys
import time
from pathlib import Path

import requests


# Colors for output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def log(message, color=Colors.RESET):
    print(f"{color}{message}{Colors.RESET}")


def test_agent_build():
    """Test building the Go agent"""
    log("🔨 Testing agent build...", Colors.BLUE)

    try:
        # Check if Go is installed
        result = subprocess.run(
            sanitize_cmd(["go", "version"], capture_output=True, text=True)
        )
        if result.returncode != 0:
            log("❌ Go is not installed", Colors.RED)
            return False

        log(f"✅ Go version: {result.stdout.strip()}", Colors.GREEN)

        # Build the agent
        result = subprocess.run(
            sanitize_cmd(["go", "build", "-o", "platform_agent", "platform_agent.go"]),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            log(f"❌ Build failed: {result.stderr}", Colors.RED)
            return False

        log("✅ Agent built successfully", Colors.GREEN)
        return True

    except Exception as e:
        log(f"❌ Build error: {e}", Colors.RED)
        return False


def test_agent_help():
    """Test agent help command"""
    log("📖 Testing agent help...", Colors.BLUE)

    try:
        result = subprocess.run(  # nosec B603
            ["./platform_agent", "--help"], capture_output=True, text=True
        )

        if result.returncode != 0:
            log(f"❌ Help command failed: {result.stderr}", Colors.RED)
            return False

        if "Usage:" not in result.stdout:
            log("❌ Help output doesn't contain expected content", Colors.RED)
            return False

        log("✅ Help command works", Colors.GREEN)
        return True

    except Exception as e:
        log(f"❌ Help test error: {e}", Colors.RED)
        return False


def test_simple_command():
    """Test simple command execution"""
    log("⚡ Testing simple command...", Colors.BLUE)

    try:
        # Use shell=False and validate input to prevent command injection
        cmd = "echo 'Hello from agent'"
        if any(char in cmd for char in [";", "&", "|", "`", "$", "(", ")", "<", ">"]):
            log("❌ Invalid characters in command", Colors.RED)
            return False

        result = subprocess.run(
            sanitize_cmd(["./platform_agent", cmd]),
            capture_output=True,
            text=True,
            shell=False,  # Explicitly disable shell
        )

        if result.returncode != 0:
            log(f"❌ Simple command failed: {result.stderr}", Colors.RED)
            return False

        if "Hello from agent" not in result.stdout:
            log("❌ Command output not found", Colors.RED)
            return False

        log("✅ Simple command works", Colors.GREEN)
        return True

    except Exception as e:
        log(f"❌ Simple command error: {e}", Colors.RED)
        return False


def test_rune_execution():
    """Test rune execution"""
    log("🔮 Testing rune execution...", Colors.BLUE)

    # Create a simple test rune
    test_rune = {
        "name": "Test Rune",
        "description": "Simple test rune",
        "commands": ["echo 'Command 1'", "echo 'Command 2'", "echo 'Command 3'"],
        "validation": {"timeout_seconds": 30, "stop_on_failure": False},
    }

    rune_file = "test_rune.json"
    with open(rune_file, "w") as f:
        json.dump(test_rune, f, indent=2)

    try:
        # Validate rune file path to prevent path traversal
        if not os.path.exists(rune_file) or not rune_file.endswith(".json"):
            log("❌ Invalid rune file", Colors.RED)
            return False

        result = subprocess.run(
            sanitize_cmd(["./platform_agent", "--rune", rune_file]),
            capture_output=True,
            text=True,
            shell=False,  # Explicitly disable shell
        )

        if result.returncode != 0:
            log(f"❌ Rune execution failed: {result.stderr}", Colors.RED)
            return False

        # Check for results file
        results_files = list(Path(".").glob("rune_results_*.json"))
        if not results_files:
            log("❌ No results file generated", Colors.RED)
            return False

        # Read results
        with open(results_files[0], "r") as f:
            results = json.load(f)

        if len(results) != 3:
            log(f"❌ Expected 3 results, got {len(results)}", Colors.RED)
            return False

        success_count = sum(1 for r in results if r.get("success", False))
        if success_count != 3:
            log(f"❌ Expected 3 successful commands, got {success_count}", Colors.RED)
            return False

        log("✅ Rune execution works", Colors.GREEN)

        # Clean up
        os.remove(rune_file)
        for file in results_files:
            os.remove(file)

        return True

    except Exception as e:
        log(f"❌ Rune execution error: {e}", Colors.RED)
        return False


def test_command_sanitization():
    """Test command sanitization"""
    log("🛡️ Testing command sanitization...", Colors.BLUE)

    dangerous_commands = [
        "rm -rf /",
        "shutdown -h now",
        "dd if=/dev/zero of=/dev/sda",
        "mkfs.ext4 /dev/sda1",
    ]

    for cmd in dangerous_commands:
        try:
            # Validate command to prevent command injection
            if any(
                char in cmd for char in [";", "&", "|", "`", "$", "(", ")", "<", ">"]
            ):
                log(f"❌ Invalid characters in command: {cmd}", Colors.RED)
                return False

            result = subprocess.run(
                sanitize_cmd(["./platform_agent", cmd]),
                capture_output=True,
                text=True,
                shell=False,  # Explicitly disable shell
            )

            # Should be blocked
            if "blocked" in result.stdout or "denied" in result.stdout:
                log(f"✅ Blocked dangerous command: {cmd}", Colors.GREEN)
            else:
                log(f"❌ Failed to block: {cmd}", Colors.RED)
                return False

        except Exception as e:
            log(f"❌ Sanitization test error: {e}", Colors.RED)
            return False

    log("✅ Command sanitization works", Colors.GREEN)
    return True


def test_api_integration():
    """Test API integration"""
    log("🌐 Testing API integration...", Colors.BLUE)

    # Check if MLOps platform is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            log("❌ MLOps platform not responding", Colors.RED)
            return False
    except requests.exceptions.RequestException:
        log("⚠️ MLOps platform not running, skipping API tests", Colors.YELLOW)
        return True

    # Test rune execution via API
    try:
        rune_request = {
            "commands": ["echo 'API test'", "echo 'API test 2'"],
            "name": "API Test Rune",
            "description": "Testing API integration",
            "timeout_seconds": 30,
        }

        response = requests.post(
            "http://localhost:8000/rune/execute", json=rune_request, timeout=10
        )

        if response.status_code != 200:
            log(f"❌ API rune execution failed: {response.status_code}", Colors.RED)
            return False

        result = response.json()
        execution_id = result.get("execution_id")

        if not execution_id:
            log("❌ No execution ID returned", Colors.RED)
            return False

        log(f"✅ API rune execution started: {execution_id}", Colors.GREEN)

        # Wait for completion
        for _ in range(10):
            time.sleep(1)
            response = requests.get(
                f"http://localhost:8000/rune/status/{execution_id}", timeout=10
            )
            if response.status_code == 200:
                status = response.json()
                if status["status"] in ["completed", "failed"]:
                    log(f"✅ Rune execution {status['status']}", Colors.GREEN)
                    break

        return True

    except Exception as e:
        log(f"❌ API integration error: {e}", Colors.RED)
        return False


def run_all_tests():
    """Run all tests"""
    log("🚀 Starting Platform Agent Tests", Colors.BLUE)
    log("=" * 40, Colors.BLUE)

    tests = [
        ("Build", test_agent_build),
        ("Help", test_agent_help),
        ("Simple Command", test_simple_command),
        ("Rune Execution", test_rune_execution),
        ("Command Sanitization", test_command_sanitization),
        ("API Integration", test_api_integration),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        log(f"\n🧪 {test_name} Test", Colors.BLUE)
        try:
            if test_func():
                passed += 1
                log(f"✅ {test_name} PASSED", Colors.GREEN)
            else:
                log(f"❌ {test_name} FAILED", Colors.RED)
        except Exception as e:
            log(f"❌ {test_name} ERROR: {e}", Colors.RED)

    log(f"\n📊 Test Results: {passed}/{total} passed", Colors.BLUE)

    if passed == total:
        log("🎉 All tests passed!", Colors.GREEN)
        return True
    else:
        log("⚠️ Some tests failed", Colors.YELLOW)
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
