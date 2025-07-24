#!/usr/bin/env python3
"""
Test Script for MCP Tool Executor
================================

This script tests the MCP tool executor functionality to ensure
everything is working correctly.
"""

import json
import os
import sys

# Add the unified-api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'unified-api'))

from logic.executor import run_tool_command, validate_command, get_command_info

def test_executor():
    """Test the executor functionality"""
    print("🧪 Testing MCP Tool Executor")
    print("=" * 50)
    
    # Test 1: Command validation
    print("\n1. Testing command validation...")
    test_commands = [
        "echo 'Hello World'",
        "ls -la",
        "rm -rf /",  # This should be rejected
        "sudo shutdown",  # This should be rejected
    ]
    
    for cmd in test_commands:
        validation = validate_command(cmd)
        status = "✅" if validation["valid"] else "❌"
        print(f"   {status} {cmd}")
        if not validation["valid"]:
            print(f"      Reason: {validation['error']}")
    
    # Test 2: Command analysis
    print("\n2. Testing command analysis...")
    for cmd in test_commands[:2]:  # Only test valid commands
        info = get_command_info(cmd)
        print(f"   📊 {cmd}")
        print(f"      Category: {info['category']}")
        print(f"      Complexity: {info['estimated_complexity']}")
        print(f"      Length: {info['command_length']} chars")
    
    # Test 3: Command execution
    print("\n3. Testing command execution...")
    test_executions = [
        "echo 'Hello from MCP Tool Executor!'",
        "date",
        "whoami",
        "pwd",
    ]
    
    for cmd in test_executions:
        print(f"   🔧 Executing: {cmd}")
        result = run_tool_command(cmd)
        print(f"      Status: {'✅ Success' if result['success'] else '❌ Failed'}")
        print(f"      Return Code: {result['returncode']}")
        print(f"      Execution Time: {result['execution_time']}s")
        if result['stdout']:
            print(f"      Output: {result['stdout'].strip()}")
        if result['stderr']:
            print(f"      Error: {result['stderr'].strip()}")
        print()
    
    # Test 4: Check saved tools
    print("4. Checking saved MCP tools...")
    mcp_dir = "db/mcp_tools"
    if os.path.exists(mcp_dir):
        tools = [f for f in os.listdir(mcp_dir) if f.endswith('.json')]
        print(f"   📁 Found {len(tools)} saved tools:")
        for tool_file in tools:
            tool_path = os.path.join(mcp_dir, tool_file)
            with open(tool_path, 'r') as f:
                tool_data = json.load(f)
            print(f"      🔧 {tool_data['name']}: {tool_data['description']}")
    else:
        print("   ❌ No MCP tools directory found")
    
    print("\n✅ MCP Tool Executor test completed!")

if __name__ == "__main__":
    test_executor() 