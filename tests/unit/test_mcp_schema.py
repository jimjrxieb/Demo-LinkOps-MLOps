#!/usr/bin/env python3
"""
MCP Tool Schema Test Suite
=========================

This script tests the MCP tool schema validation with various test cases
to ensure proper validation and error handling.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Change to the project root directory for proper imports
os.chdir(project_root)

# Import the modules using the correct path
import sys

sys.path.insert(0, str(project_root / "unified-api"))

from schemas.mcp_tool_schema import MCPTool, validate_mcp_tool_data


def test_valid_tools():
    """Test valid MCP tool configurations."""
    print("🧪 Testing Valid MCP Tools...")

    valid_tools = [
        {
            "name": "restart_apache",
            "description": "Restart Apache web server gracefully",
            "task_type": "sysadmin",
            "command": "sudo systemctl restart apache2",
            "tags": ["linux", "apache", "restart"],
            "auto": True,
        },
        {
            "name": "check_disk_space",
            "description": "Check available disk space",
            "task_type": "monitoring",
            "command": "df -h",
            "tags": ["disk", "space"],
            "auto": False,
        },
        {
            "name": "system_status",
            "description": "Display system status and resource usage",
            "task_type": "monitoring",
            "command": "uptime && free -h && df -h .",
            "tags": ["system", "status", "monitoring"],
            "auto": True,
        },
    ]

    for i, tool_data in enumerate(valid_tools, 1):
        try:
            tool = MCPTool(**tool_data)
            print(f"✅ Test {i}: Valid tool '{tool.name}' created successfully")
            print(f"   - Auto: {tool.auto}")
            print(f"   - Tags: {tool.tags}")
        except Exception as e:
            print(f"❌ Test {i}: Failed to create valid tool: {str(e)}")

    print()


def test_invalid_names():
    """Test invalid tool names."""
    print("🧪 Testing Invalid Tool Names...")

    invalid_names = [
        {
            "name": "",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
        },
        {
            "name": "tool with spaces",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
        },
        {
            "name": "tool@invalid",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
        },
        {
            "name": "system",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
        },
        {
            "name": "admin",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
        },
        {
            "name": "root",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
        },
    ]

    for i, tool_data in enumerate(invalid_names, 1):
        try:
            MCPTool(**tool_data)
            print(f"❌ Test {i}: Should have failed for name '{tool_data['name']}'")
        except Exception as e:
            print(
                f"✅ Test {i}: Correctly rejected invalid name '{tool_data['name']}': {str(e)}"
            )

    print()


def test_dangerous_commands():
    """Test dangerous command detection."""
    print("🧪 Testing Dangerous Command Detection...")

    dangerous_commands = [
        {
            "name": "dangerous1",
            "description": "Test",
            "task_type": "test",
            "command": "rm -rf /",
        },
        {
            "name": "dangerous2",
            "description": "Test",
            "task_type": "test",
            "command": "dd if=/dev/zero of=/dev/sda",
        },
        {
            "name": "dangerous3",
            "description": "Test",
            "task_type": "test",
            "command": "chmod 777 /etc/passwd",
        },
        {
            "name": "dangerous4",
            "description": "Test",
            "task_type": "test",
            "command": "echo 'test' > /etc/passwd",
        },
        {
            "name": "dangerous5",
            "description": "Test",
            "task_type": "test",
            "command": "ls | bash",
        },
    ]

    for i, tool_data in enumerate(dangerous_commands, 1):
        try:
            MCPTool(**tool_data)
            print(
                f"❌ Test {i}: Should have failed for dangerous command: {tool_data['command']}"
            )
        except Exception as e:
            print(f"✅ Test {i}: Correctly rejected dangerous command: {str(e)}")

    print()


def test_invalid_tags():
    """Test invalid tag validation."""
    print("🧪 Testing Invalid Tags...")

    invalid_tag_tests = [
        {
            "name": "test1",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
            "tags": ["valid-tag", "tag with spaces", "invalid@tag"],
        },
        {
            "name": "test2",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
            "tags": [
                "",
                "   ",
                "very-long-tag-name-that-exceeds-the-maximum-length-allowed",
            ],
        },
        {
            "name": "test3",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
            "tags": ["duplicate", "duplicate", "unique"],
        },
    ]

    for i, tool_data in enumerate(invalid_tag_tests, 1):
        try:
            tool = MCPTool(**tool_data)
            print(f"✅ Test {i}: Tags processed successfully: {tool.tags}")
        except Exception as e:
            print(f"❌ Test {i}: Tag validation failed: {str(e)}")

    print()


def test_auto_execution_validation():
    """Test auto-execution validation."""
    print("🧪 Testing Auto-Execution Validation...")

    auto_tests = [
        {
            "name": "interactive_tool",
            "description": "Interactive tool",
            "task_type": "test",
            "command": "read -p 'Continue? (y/n): '",
            "auto": True,
        },
        {
            "name": "prompt_tool",
            "description": "Tool with prompt",
            "task_type": "test",
            "command": "echo 'Do you want to continue?' && read response",
            "auto": True,
        },
    ]

    for i, tool_data in enumerate(auto_tests, 1):
        try:
            MCPTool(**tool_data)
            print(
                f"❌ Test {i}: Should have failed for interactive auto tool: {tool_data['command']}"
            )
        except Exception as e:
            print(f"✅ Test {i}: Correctly rejected interactive auto tool: {str(e)}")

    print()


def test_field_validation():
    """Test field length and type validation."""
    print("🧪 Testing Field Validation...")

    field_tests = [
        {
            "name": "a" * 101,  # Too long name
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
        },
        {
            "name": "test",
            "description": "a" * 501,  # Too long description
            "task_type": "test",
            "command": "echo test",
        },
        {
            "name": "test",
            "description": "Test",
            "task_type": "a" * 51,  # Too long task type
            "command": "echo test",
        },
        {
            "name": "test",
            "description": "Test",
            "task_type": "test",
            "command": "a" * 2001,  # Too long command
        },
    ]

    for i, tool_data in enumerate(field_tests, 1):
        try:
            MCPTool(**tool_data)
            print(f"❌ Test {i}: Should have failed for field validation")
        except Exception as e:
            print(f"✅ Test {i}: Correctly rejected invalid field: {str(e)}")

    print()


def test_utility_functions():
    """Test utility validation functions."""
    print("🧪 Testing Utility Functions...")

    try:
        # Test valid data
        valid_data = {
            "name": "test_tool",
            "description": "Test tool",
            "task_type": "test",
            "command": "echo test",
            "tags": ["test"],
            "auto": False,
        }

        tool = validate_mcp_tool_data(valid_data)
        print(f"✅ Utility function: Valid tool created: {tool.name}")

        # Test invalid data
        invalid_data = {
            "name": "invalid@name",
            "description": "Test",
            "task_type": "test",
            "command": "echo test",
        }

        tool = validate_mcp_tool_data(invalid_data)
        print("❌ Utility function: Should have failed for invalid data")

    except Exception as e:
        print(f"✅ Utility function: Correctly caught validation error: {str(e)}")

    print()


def main():
    """Run all tests."""
    print("🚀 MCP Tool Schema Test Suite")
    print("=" * 50)
    print()

    test_valid_tools()
    test_invalid_names()
    test_dangerous_commands()
    test_invalid_tags()
    test_auto_execution_validation()
    test_field_validation()
    test_utility_functions()

    print("🎉 Test suite completed!")


if __name__ == "__main__":
    main()
