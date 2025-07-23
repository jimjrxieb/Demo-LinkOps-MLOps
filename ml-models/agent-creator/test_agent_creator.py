#!/usr/bin/env python3
"""
Test script for the Agent Creator service.
"""

import json
import time

import requests


def test_health_endpoint():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False


def test_supported_agents():
    """Test the supported agents endpoint."""
    print("🔍 Testing supported agents endpoint...")
    try:
        response = requests.get("http://localhost:8001/supported-agents")
        if response.status_code == 200:
            data = response.json()
            print("✅ Supported agents endpoint working")
            print(f"   Agent types: {data.get('agent_types', [])}")
            return True
        else:
            print(f"❌ Supported agents endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Supported agents endpoint error: {e}")
        return False


def test_agent_templates():
    """Test the agent templates endpoint."""
    print("🔍 Testing agent templates endpoint...")
    try:
        response = requests.get("http://localhost:8001/agent-templates")
        if response.status_code == 200:
            data = response.json()
            print("✅ Agent templates endpoint working")
            print(f"   Templates: {list(data.keys())}")
            return True
        else:
            print(f"❌ Agent templates endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent templates endpoint error: {e}")
        return False


def test_base_agent_generation():
    """Test base agent generation."""
    print("🔍 Testing base agent generation...")
    try:
        response = requests.post(
            "http://localhost:8001/generate-agent/",
            data={
                "agent_type": "base",
                "agent_name": "TestBaseAgent",
                "tools": "",
                "capabilities": "",
                "security_level": "medium",
            },
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Base agent generation working")
            print(f"   Agent type: {data.get('agent_type')}")
            print(f"   Agent name: {data.get('agent_name')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Base agent generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Base agent generation error: {e}")
        return False


def test_commandbot_generation():
    """Test commandbot generation."""
    print("🔍 Testing commandbot generation...")
    try:
        response = requests.post(
            "http://localhost:8001/generate-agent/",
            data={
                "agent_type": "commandbot",
                "agent_name": "SecureShell",
                "tools": "ls,pwd,whoami,echo",
                "capabilities": "command_execution,security_validation",
                "security_level": "high",
            },
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Commandbot generation working")
            print(f"   Agent type: {data.get('agent_type')}")
            print(f"   Tools: {data.get('tools')}")
            print(f"   Security level: {data.get('security_level')}")
            return True
        else:
            print(f"❌ Commandbot generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Commandbot generation error: {e}")
        return False


def test_taskbot_generation():
    """Test taskbot generation."""
    print("🔍 Testing taskbot generation...")
    try:
        response = requests.post(
            "http://localhost:8001/generate-agent/",
            data={
                "agent_type": "taskbot",
                "agent_name": "DataProcessor",
                "tools": "pandas,numpy,requests",
                "capabilities": "data_processing,file_operations",
                "security_level": "medium",
            },
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Taskbot generation working")
            print(f"   Agent type: {data.get('agent_type')}")
            print(f"   Tools: {data.get('tools')}")
            print(f"   Capabilities: {data.get('capabilities')}")
            return True
        else:
            print(f"❌ Taskbot generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Taskbot generation error: {e}")
        return False


def test_assistant_generation():
    """Test assistant generation."""
    print("🔍 Testing assistant generation...")
    try:
        response = requests.post(
            "http://localhost:8001/generate-agent/",
            data={
                "agent_type": "assistant",
                "agent_name": "HelpBot",
                "tools": "search,calculate,format",
                "capabilities": "conversation,information_retrieval",
                "security_level": "medium",
            },
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Assistant generation working")
            print(f"   Agent type: {data.get('agent_type')}")
            print(f"   Tools: {data.get('tools')}")
            print(f"   Capabilities: {data.get('capabilities')}")
            return True
        else:
            print(f"❌ Assistant generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Assistant generation error: {e}")
        return False


def test_workflow_agent_generation():
    """Test workflow agent generation."""
    print("🔍 Testing workflow agent generation...")
    try:
        # Define workflow steps
        steps = [
            {
                "step": "extract",
                "action": "read_data",
                "params": {"source": "input.csv"},
            },
            {
                "step": "transform",
                "action": "process_data",
                "params": {"transformations": ["clean", "validate"]},
            },
            {"step": "load", "action": "save", "params": {"destination": "output.csv"}},
        ]

        response = requests.post(
            "http://localhost:8001/generate-workflow-agent/",
            data={
                "workflow_name": "DataPipeline",
                "steps": json.dumps(steps),
                "triggers": "schedule,manual,event",
                "error_handling": "retry",
            },
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Workflow agent generation working")
            print(f"   Workflow name: {data.get('workflow_name')}")
            print(f"   Steps: {len(data.get('steps', []))}")
            print(f"   Triggers: {data.get('triggers')}")
            return True
        else:
            print(f"❌ Workflow agent generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Workflow agent generation error: {e}")
        return False


def test_agent_validation():
    """Test agent configuration validation."""
    print("🔍 Testing agent validation...")
    try:
        response = requests.post(
            "http://localhost:8001/validate-agent/",
            data={
                "agent_type": "commandbot",
                "tools": "ls,pwd,whoami",
                "security_level": "medium",
            },
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Agent validation working")
            print(f"   Valid: {data.get('valid')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Agent validation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent validation error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Agent Creator Test Suite")
    print("=" * 40)

    # Wait for service to start
    print("⏳ Waiting for service to start...")
    time.sleep(5)

    tests = [
        test_health_endpoint,
        test_supported_agents,
        test_agent_templates,
        test_base_agent_generation,
        test_commandbot_generation,
        test_taskbot_generation,
        test_assistant_generation,
        test_workflow_agent_generation,
        test_agent_validation,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("📊 Test Results")
    print("=" * 20)
    print(f"Passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")

    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
