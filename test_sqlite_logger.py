#!/usr/bin/env python3
"""
SQLite Execution Logger Test Script
==================================

This script demonstrates the new SQLite-based execution logging system
and compares it with the previous JSON file-based approach.
"""

import sys
import os
import time
from datetime import datetime

# Add the unified-api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'unified-api'))

from logic.execution_logger import (
    init_logger, 
    log_execution, 
    get_logs, 
    get_execution_stats, 
    get_tool_performance,
    cleanup_old_logs
)
from logic.executor import run_tool_command

def test_sqlite_logger():
    """Test the SQLite execution logger functionality"""
    print("🧪 Testing SQLite Execution Logger")
    print("=" * 50)
    
    # Test 1: Initialize logger
    print("\n1️⃣ Initializing SQLite logger...")
    try:
        init_logger()
        print("   ✅ SQLite logger initialized successfully")
    except Exception as e:
        print(f"   ❌ Failed to initialize logger: {e}")
        return
    
    # Test 2: Log some test executions
    print("\n2️⃣ Logging test executions...")
    
    test_executions = [
        {
            "tool_name": "hello-world",
            "command": "echo 'Hello from SQLite logger!'",
            "stdout": "Hello from SQLite logger!",
            "stderr": "",
            "returncode": 0,
            "duration_ms": 25,
            "success": True
        },
        {
            "tool_name": "system-info",
            "command": "uname -a",
            "stdout": "Linux test-system 5.15.0 x86_64 GNU/Linux",
            "stderr": "",
            "returncode": 0,
            "duration_ms": 45,
            "success": True
        },
        {
            "tool_name": "failed-command",
            "command": "nonexistent-command",
            "stdout": "",
            "stderr": "command not found: nonexistent-command",
            "returncode": 127,
            "duration_ms": 15,
            "success": False
        },
        {
            "tool_name": "process-list",
            "command": "ps aux | head -5",
            "stdout": "USER PID %CPU %MEM COMMAND\nroot 1 0.0 0.1 /sbin/init",
            "stderr": "",
            "returncode": 0,
            "duration_ms": 120,
            "success": True
        }
    ]
    
    for i, execution in enumerate(test_executions, 1):
        success = log_execution(**execution)
        status = "✅" if success else "❌"
        print(f"   {status} Logged execution {i}: {execution['tool_name']}")
    
    # Test 3: Get execution statistics
    print("\n3️⃣ Getting execution statistics...")
    stats = get_execution_stats()
    
    print(f"   📊 Total executions: {stats['total_executions']}")
    print(f"   ✅ Successful: {stats['successful_executions']}")
    print(f"   ❌ Failed: {stats['failed_executions']}")
    print(f"   📈 Success rate: {stats['success_rate']}%")
    print(f"   ⏱️ Average time: {stats['average_execution_time_ms']}ms")
    
    if stats['most_used_tools']:
        print("   🔧 Most used tools:")
        for tool_name, count in stats['most_used_tools']:
            print(f"      - {tool_name}: {count} executions")
    
    # Test 4: Get recent activity
    print("\n4️⃣ Recent activity:")
    recent = stats['recent_activity']
    for i, activity in enumerate(recent[:3], 1):  # Show last 3
        status = "✅" if activity['success'] else "❌"
        print(f"   {i}. {status} {activity['tool_name']} ({activity['duration_ms']}ms)")
    
    # Test 5: Get tool-specific performance
    print("\n5️⃣ Tool-specific performance:")
    for tool_name in ["hello-world", "system-info", "process-list"]:
        performance = get_tool_performance(tool_name)
        print(f"   📊 {tool_name}:")
        print(f"      - Total: {performance['total_executions']}")
        print(f"      - Success rate: {performance['success_rate']}%")
        print(f"      - Avg time: {performance['average_duration_ms']}ms")
        print(f"      - Min/Max: {performance['min_duration_ms']}ms / {performance['max_duration_ms']}ms")
    
    # Test 6: Get filtered logs
    print("\n6️⃣ Filtered logs by tool:")
    for tool_name in ["hello-world", "system-info"]:
        logs = get_logs(limit=5, tool_name=tool_name)
        print(f"   📋 {tool_name} logs ({len(logs)} entries):")
        for log in logs[:2]:  # Show first 2
            status = "✅" if log['success'] else "❌"
            print(f"      - {status} {log['command'][:30]}... ({log['duration_ms']}ms)")
    
    # Test 7: Integration with executor
    print("\n7️⃣ Integration with executor:")
    try:
        result = run_tool_command("echo 'Testing integration'")
        success = log_execution(
            tool_name="integration-test",
            command="echo 'Testing integration'",
            stdout=result['stdout'],
            stderr=result['stderr'],
            returncode=result['returncode'],
            duration_ms=int(result['execution_time'] * 1000),
            success=result['success']
        )
        print(f"   {'✅' if success else '❌'} Integrated execution logged")
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
    
    print("\n✅ SQLite logger test completed!")

def compare_with_json_logging():
    """Compare SQLite logging with JSON file-based approach"""
    print("\n" + "=" * 50)
    print("📊 SQLite vs JSON Logging Comparison")
    print("=" * 50)
    
    print("\n🔍 Performance Comparison:")
    print("   SQLite Advantages:")
    print("   ✅ Faster queries with indexes")
    print("   ✅ Atomic transactions")
    print("   ✅ Better data integrity")
    print("   ✅ SQL querying capabilities")
    print("   ✅ Automatic cleanup functions")
    print("   ✅ Smaller storage footprint")
    
    print("\n   JSON File Advantages:")
    print("   ❌ Human-readable files")
    print("   ❌ Easy to backup individual files")
    print("   ❌ No database setup required")
    
    print("\n📈 Recommended: SQLite for production use")

if __name__ == "__main__":
    test_sqlite_logger()
    compare_with_json_logging() 