#!/usr/bin/env python3
"""
MCP Tool Executor - Complete Workflow Demo
=========================================

This script demonstrates the complete workflow from creating MCP tools
to executing them and viewing results.
"""

import json
import os
import sys
import time

# Add the unified-api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "unified-api"))

from logic.executor import get_command_info, run_tool_command, validate_command


def create_sample_tool(name, description, command, tags=None):
    """Create a sample MCP tool"""
    if tags is None:
        tags = []

    tool = {
        "name": name,
        "description": description,
        "task_type": "command",
        "command": command,
        "tags": tags,
    }

    # Ensure directory exists
    os.makedirs("db/mcp_tools", exist_ok=True)

    # Save tool
    tool_path = f"db/mcp_tools/{name}.json"
    with open(tool_path, "w") as f:
        json.dump(tool, f, indent=2)

    print(f"✅ Created tool: {name}")
    return tool


def list_tools():
    """List all available tools"""
    tools = []
    mcp_dir = "db/mcp_tools"

    if os.path.exists(mcp_dir):
        for filename in os.listdir(mcp_dir):
            if filename.endswith(".json"):
                tool_path = os.path.join(mcp_dir, filename)
                with open(tool_path) as f:
                    tool = json.load(f)
                    tools.append(tool)

    return tools


def execute_tool(tool_name):
    """Execute a saved tool"""
    tool_path = f"db/mcp_tools/{tool_name}.json"

    if not os.path.exists(tool_path):
        print(f"❌ Tool '{tool_name}' not found")
        return None

    # Load tool
    with open(tool_path) as f:
        tool = json.load(f)

    print(f"\n🔧 Executing tool: {tool['name']}")
    print(f"   Command: {tool['command']}")
    print(f"   Description: {tool['description']}")

    # Execute
    result = run_tool_command(tool["command"])

    # Display results
    print("\n📊 Results:")
    print(f"   Status: {'✅ Success' if result['success'] else '❌ Failed'}")
    print(f"   Return Code: {result['returncode']}")
    print(f"   Execution Time: {result['execution_time']}s")

    if result["stdout"]:
        print("\n📤 Standard Output:")
        print(f"   {result['stdout'].strip()}")

    if result["stderr"]:
        print("\n📥 Error Output:")
        print(f"   {result['stderr'].strip()}")

    return result


def demo_workflow():
    """Demonstrate the complete MCP tool workflow"""
    print("🚀 MCP Tool Executor - Complete Workflow Demo")
    print("=" * 60)

    # Step 1: Create sample tools
    print("\n1️⃣ Creating sample MCP tools...")

    tools_to_create = [
        {
            "name": "hello-world",
            "description": "Simple hello world demonstration",
            "command": "echo 'Hello from MCP Tool Executor!' && echo 'Current time:' && date",
            "tags": ["demo", "hello", "basic"],
        },
        {
            "name": "system-status",
            "description": "Check system status and resources",
            "command": "echo '=== System Status ===' && uptime && echo '=== Memory ===' && free -h && echo '=== Disk ===' && df -h .",
            "tags": ["system", "monitoring", "status"],
        },
        {
            "name": "network-info",
            "description": "Display network information",
            "command": "echo '=== Network Interfaces ===' && ip addr show && echo '=== Routing ===' && ip route show",
            "tags": ["network", "info", "system"],
        },
    ]

    for tool_data in tools_to_create:
        create_sample_tool(**tool_data)

    # Step 2: List available tools
    print("\n2️⃣ Available tools:")
    tools = list_tools()
    for i, tool in enumerate(tools, 1):
        print(f"   {i}. {tool['name']}: {tool['description']}")
        print(f"      Tags: {', '.join(tool['tags'])}")

    # Step 3: Execute tools
    print("\n3️⃣ Executing tools...")

    for tool in tools:
        print(f"\n{'='*50}")
        result = execute_tool(tool["name"])

        if result and result["success"]:
            print(f"✅ {tool['name']} executed successfully!")
        else:
            print(f"❌ {tool['name']} execution failed!")

        time.sleep(1)  # Brief pause between executions

    # Step 4: Demonstrate command validation
    print(f"\n{'='*50}")
    print("4️⃣ Testing command validation...")

    test_commands = [
        "echo 'Safe command'",
        "ls -la",
        "rm -rf /",  # Should be blocked
        "sudo shutdown",  # Should be blocked
    ]

    for cmd in test_commands:
        validation = validate_command(cmd)
        status = "✅" if validation["valid"] else "❌"
        print(f"   {status} {cmd}")
        if not validation["valid"]:
            print(f"      Blocked: {validation['error']}")

    # Step 5: Show command analysis
    print(f"\n{'='*50}")
    print("5️⃣ Command analysis examples...")

    for cmd in ["echo 'test'", "ls -la /tmp", "grep -r 'pattern' ."]:
        info = get_command_info(cmd)
        print(f"   📊 {cmd}")
        print(f"      Category: {info['category']}")
        print(f"      Complexity: {info['estimated_complexity']}")
        print(f"      Length: {info['command_length']} chars")

    print(f"\n{'='*50}")
    print("🎉 Demo completed successfully!")
    print("\n📋 What you've seen:")
    print("   ✅ MCP tool creation and storage")
    print("   ✅ Tool listing and management")
    print("   ✅ Secure command execution")
    print("   ✅ Real-time output capture")
    print("   ✅ Command validation and security")
    print("   ✅ Command analysis and categorization")
    print("\n🚀 The AI platform now has the power to execute tools!")


if __name__ == "__main__":
    demo_workflow()
