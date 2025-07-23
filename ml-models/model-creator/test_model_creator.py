#!/usr/bin/env python3
"""
Test script for the ML Model Creator service.
"""

import json
import time

import requests


def test_health_endpoint():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8002/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False


def test_supported_models():
    """Test the supported models endpoint."""
    print("🔍 Testing supported models endpoint...")
    try:
        response = requests.get("http://localhost:8002/supported-models")
        if response.status_code == 200:
            data = response.json()
            print("✅ Supported models endpoint working")
            print(f"   Model types: {data.get('model_types', [])}")
            return True
        else:
            print(f"❌ Supported models endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Supported models endpoint error: {e}")
        return False


def test_supported_agents():
    """Test the supported agents endpoint."""
    print("🔍 Testing supported agents endpoint...")
    try:
        response = requests.get("http://localhost:8002/supported-agents")
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


def test_model_generation():
    """Test model generation endpoint."""
    print("🔍 Testing model generation...")
    try:
        response = requests.post(
            "http://localhost:8002/generate-model/",
            data={
                "model_type": "classification",
                "target_column": "target",
                "algorithm": "random_forest",
            },
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Model generation working")
            print(f"   Model type: {data.get('model_type')}")
            print(f"   Algorithm: {data.get('algorithm')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Model generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Model generation error: {e}")
        return False


def test_agent_generation():
    """Test agent generation endpoint."""
    print("🔍 Testing agent generation...")
    try:
        response = requests.post(
            "http://localhost:8002/generate-agent/",
            data={
                "agent_type": "task_evaluator",
                "capabilities": "classification,scoring,recommendation",
                "model_type": "classification",
            },
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Agent generation working")
            print(f"   Agent type: {data.get('agent_type')}")
            print(f"   Capabilities: {data.get('capabilities')}")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Agent generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Agent generation error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 ML Model Creator Test Suite")
    print("=" * 40)

    # Wait for service to start
    print("⏳ Waiting for service to start...")
    time.sleep(5)

    tests = [
        test_health_endpoint,
        test_supported_models,
        test_supported_agents,
        test_model_generation,
        test_agent_generation,
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
