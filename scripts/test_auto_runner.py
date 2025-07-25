#!/usr/bin/env python3
"""
Auto Runner Test Suite
======================

This script tests the Auto Runner backend with various scenarios including:
- Valid tool execution
- Security validation
- Error handling
- Logging functionality
"""

import json
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Change to the project root directory for proper imports
os.chdir(project_root)

# Import the modules using the correct path
sys.path.insert(0, str(project_root / "unified-api"))

from executor.auto_runner import get_execution_history, run_tool


def create_test_tool(name: str, command: str, auto: bool = True) -> None:
    """Create a test MCP tool for testing."""
    tool_data = {
        "name": name,
        "description": f"Test tool: {name}",
        "task_type": "test",
        "command": command,
        "tags": ["test", "auto-runner"],
        "auto": auto,
    }

    # Create the tool file
    tool_dir = Path("db/mcp_tools")
    tool_dir.mkdir(parents=True, exist_ok=True)

    tool_file = tool_dir / f"{name}.json"
    with open(tool_file, "w") as f:
        json.dump(tool_data, f, indent=2)

    print(f"✅ Created test tool: {name}")


def test_valid_execution():
    """Test execution of valid tools."""
    print("🧪 Testing Valid Tool Execution...")

    # Create a simple test tool
    create_test_tool("echo_test", "echo 'Hello from Auto Runner!'")

    try:
        result = run_tool("echo_test")
        print(f"✅ Execution successful: {result['success']}")
        print(f"📊 Return code: {result['returncode']}")
        print(f"📤 Output: {result['stdout']}")
        print(f"⏱️  Execution time: {result['execution_time']:.2f}s")

        if result["success"]:
            print("✅ Valid execution test passed")
        else:
            print("❌ Valid execution test failed")

    except Exception as e:
        print(f"❌ Valid execution test failed: {e}")

    print()


def test_auto_execution_check():
    """Test that non-auto tools are rejected."""
    print("🧪 Testing Auto Execution Check...")

    # Create a tool with auto=False
    create_test_tool("manual_tool", "echo 'Manual tool'", auto=False)

    try:
        result = run_tool("manual_tool")
        if (
            not result["success"]
            and "not set for auto-execution" in result["error_message"]
        ):
            print("✅ Auto execution check passed - manual tool correctly rejected")
        else:
            print("❌ Auto execution check failed - manual tool was executed")

    except Exception as e:
        print(f"❌ Auto execution check failed: {e}")

    print()


def test_security_validation():
    """Test security validation of dangerous commands."""
    print("🧪 Testing Security Validation...")

    dangerous_commands = [
        ("dangerous_rm", "rm -rf /tmp/test"),
        ("dangerous_dd", "dd if=/dev/zero of=/dev/null"),
        ("dangerous_chmod", "chmod 777 /etc/passwd"),
        ("dangerous_shutdown", "shutdown -h now"),
        ("dangerous_reboot", "reboot"),
    ]

    for name, command in dangerous_commands:
        create_test_tool(name, command, auto=True)

        try:
            result = run_tool(name)
            if (
                not result["success"]
                and "Security check failed" in result["error_message"]
            ):
                print(f"✅ Security check passed for {name}")
            else:
                print(f"❌ Security check failed for {name} - command was executed")

        except Exception as e:
            print(f"❌ Security test failed for {name}: {e}")

    print()


def test_interactive_commands():
    """Test that interactive commands are blocked."""
    print("🧪 Testing Interactive Command Blocking...")

    interactive_commands = [
        ("interactive_read", "read -p 'Enter value: ' value"),
        ("interactive_prompt", "echo 'Do you want to continue?' && read response"),
        ("interactive_confirm", "confirm 'Are you sure?'"),
    ]

    for name, command in interactive_commands:
        create_test_tool(name, command, auto=True)

        try:
            result = run_tool(name)
            if (
                not result["success"]
                and "interactive pattern" in result["error_message"]
            ):
                print(f"✅ Interactive check passed for {name}")
            else:
                print(f"❌ Interactive check failed for {name} - command was executed")

        except Exception as e:
            print(f"❌ Interactive test failed for {name}: {e}")

    print()


def test_timeout_handling():
    """Test timeout handling for long-running commands."""
    print("🧪 Testing Timeout Handling...")

    # Create a tool that sleeps longer than the timeout
    create_test_tool("timeout_test", "sleep 35", auto=True)

    try:
        result = run_tool("timeout_test")
        if not result["success"] and "timed out" in result["stderr"]:
            print("✅ Timeout handling passed - command was properly timed out")
        else:
            print(
                "❌ Timeout handling failed - command completed or failed for wrong reason"
            )

    except Exception as e:
        print(f"❌ Timeout test failed: {e}")

    print()


def test_logging_functionality():
    """Test that executions are properly logged."""
    print("🧪 Testing Logging Functionality...")

    # Create a simple tool for logging test
    create_test_tool("logging_test", "echo 'Logging test'", auto=True)

    try:
        # Get initial history count
        initial_history = get_execution_history()
        initial_count = len(initial_history)

        # Execute the tool
        run_tool("logging_test")

        # Get updated history
        updated_history = get_execution_history()
        updated_count = len(updated_history)

        if updated_count > initial_count:
            print("✅ Logging functionality passed - execution was logged")
            print(f"📊 History entries: {initial_count} → {updated_count}")

            # Check if the latest entry is our test
            latest_entry = updated_history[-1]
            if latest_entry["tool_name"] == "logging_test":
                print("✅ Latest log entry matches our test tool")
            else:
                print("❌ Latest log entry doesn't match our test tool")
        else:
            print("❌ Logging functionality failed - execution was not logged")

    except Exception as e:
        print(f"❌ Logging test failed: {e}")

    print()


def test_error_handling():
    """Test error handling for various failure scenarios."""
    print("🧪 Testing Error Handling...")

    # Test with non-existent tool
    try:
        result = run_tool("non_existent_tool")
        if not result["success"] and "not found" in result["error_message"]:
            print("✅ Non-existent tool handling passed")
        else:
            print("❌ Non-existent tool handling failed")
    except Exception as e:
        print(f"❌ Non-existent tool test failed: {e}")

    # Test with invalid command
    create_test_tool(
        "invalid_command", "invalid_command_that_does_not_exist", auto=True
    )

    try:
        result = run_tool("invalid_command")
        if not result["success"] and result["returncode"] != 0:
            print("✅ Invalid command handling passed")
        else:
            print("❌ Invalid command handling failed")
    except Exception as e:
        print(f"❌ Invalid command test failed: {e}")

    print()


def test_execution_history():
    """Test execution history functionality."""
    print("🧪 Testing Execution History...")

    try:
        # Get execution history
        history = get_execution_history(limit=10)
        print(f"📊 Retrieved {len(history)} execution records")

        if history:
            # Check structure of history entries
            latest = history[-1]
            required_fields = [
                "tool_name",
                "command",
                "timestamp",
                "returncode",
                "success",
            ]

            if all(field in latest for field in required_fields):
                print("✅ Execution history structure is correct")
            else:
                print("❌ Execution history structure is incorrect")

            # Show some recent executions
            print("📋 Recent executions:")
            for entry in history[-3:]:
                status = "✅" if entry["success"] else "❌"
                print(f"  {status} {entry['tool_name']} ({entry['timestamp']})")
        else:
            print("ℹ️  No execution history found (this is normal for first run)")

    except Exception as e:
        print(f"❌ Execution history test failed: {e}")

    print()


def cleanup_test_tools():
    """Clean up test tools created during testing."""
    print("🧹 Cleaning up test tools...")

    test_tools = [
        "echo_test",
        "manual_tool",
        "dangerous_rm",
        "dangerous_dd",
        "dangerous_chmod",
        "dangerous_shutdown",
        "dangerous_reboot",
        "interactive_read",
        "interactive_prompt",
        "interactive_confirm",
        "timeout_test",
        "logging_test",
        "invalid_command",
    ]

    tool_dir = Path("db/mcp_tools")
    cleaned_count = 0

    for tool_name in test_tools:
        tool_file = tool_dir / f"{tool_name}.json"
        if tool_file.exists():
            tool_file.unlink()
            cleaned_count += 1

    print(f"✅ Cleaned up {cleaned_count} test tools")


def main():
    """Run all tests."""
    print("🚀 Auto Runner Test Suite")
    print("=" * 50)
    print()

    # Run all tests
    test_valid_execution()
    test_auto_execution_check()
    test_security_validation()
    test_interactive_commands()
    test_timeout_handling()
    test_logging_functionality()
    test_error_handling()
    test_execution_history()

    # Cleanup
    cleanup_test_tools()

    print("🎉 Auto Runner test suite completed!")


if __name__ == "__main__":
    main()
