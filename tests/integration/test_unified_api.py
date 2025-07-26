#!/usr/bin/env python3
"""
Test Unified API
===============

Simple test script to verify all unified API endpoints are working.
"""

from datetime import datetime

import requests

# Configuration
BASE_URL = "http://localhost:9000"
TIMEOUT = 30


def test_health_endpoint():
    """Test the main health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_model_creator_health():
    """Test model creator health endpoint."""
    print("🔍 Testing model creator health...")
    try:
        response = requests.get(f"{BASE_URL}/model-creator/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model creator health: {data['status']}")
            return True
        else:
            print(f"❌ Model creator health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model creator health error: {e}")
        return False


def test_rag_health():
    """Test RAG health endpoint."""
    print("🔍 Testing RAG health...")
    try:
        response = requests.get(f"{BASE_URL}/rag/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ RAG health: {data['status']}")
            return True
        else:
            print(f"❌ RAG health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ RAG health error: {e}")
        return False


def test_agent_creator_health():
    """Test agent creator health endpoint."""
    print("🔍 Testing agent creator health...")
    try:
        response = requests.get(f"{BASE_URL}/agent-creator/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent creator health: {data['status']}")
            return True
        else:
            print(f"❌ Agent creator health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent creator health error: {e}")
        return False


def test_pipeline_health():
    """Test pipeline health endpoint."""
    print("🔍 Testing pipeline health...")
    try:
        response = requests.get(f"{BASE_URL}/pipeline/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pipeline health: {data['status']}")
            return True
        else:
            print(f"❌ Pipeline health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Pipeline health error: {e}")
        return False


def test_system_info():
    """Test system information endpoint."""
    print("🔍 Testing system info...")
    try:
        response = requests.get(f"{BASE_URL}/system", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print("✅ System info retrieved")
            print(f"   Platform: {data['system']['platform']}")
            print(f"   Version: {data['system']['version']}")
            print(f"   Services: {len(data['services'])}")
            return True
        else:
            print(f"❌ System info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ System info error: {e}")
        return False


def test_model_creator_endpoints():
    """Test model creator endpoints."""
    print("🔍 Testing model creator endpoints...")

    # Test supported models
    try:
        response = requests.get(
            f"{BASE_URL}/model-creator/supported-models", timeout=TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Supported models: {len(data['supported_models'])} types")
        else:
            print(f"❌ Supported models failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Supported models error: {e}")

    # Test algorithms
    try:
        response = requests.get(f"{BASE_URL}/model-creator/algorithms", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Algorithms: {len(data['algorithms'])} categories")
        else:
            print(f"❌ Algorithms failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Algorithms error: {e}")


def test_rag_endpoints():
    """Test RAG endpoints."""
    print("🔍 Testing RAG endpoints...")

    # Test stats
    try:
        response = requests.get(f"{BASE_URL}/rag/stats", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ RAG stats: {data['stats']['total_documents']} documents")
        else:
            print(f"❌ RAG stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ RAG stats error: {e}")

    # Test available models
    try:
        response = requests.get(f"{BASE_URL}/rag/models", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ RAG models: {len(data['models']['available_models'])} available")
        else:
            print(f"❌ RAG models failed: {response.status_code}")
    except Exception as e:
        print(f"❌ RAG models error: {e}")


def test_agent_creator_endpoints():
    """Test agent creator endpoints."""
    print("🔍 Testing agent creator endpoints...")

    # Test templates
    try:
        response = requests.get(f"{BASE_URL}/agent-creator/templates", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent templates: {len(data['templates'])} types")
        else:
            print(f"❌ Agent templates failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Agent templates error: {e}")

    # Test capabilities
    try:
        response = requests.get(
            f"{BASE_URL}/agent-creator/capabilities", timeout=TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent capabilities: {len(data['capabilities'])} available")
        else:
            print(f"❌ Agent capabilities failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Agent capabilities error: {e}")


def main():
    """Run all tests."""
    print("🚀 Testing Unified API")
    print("=" * 50)
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    tests = [
        ("Main Health", test_health_endpoint),
        ("Model Creator Health", test_model_creator_health),
        ("RAG Health", test_rag_health),
        ("Agent Creator Health", test_agent_creator_health),
        ("Pipeline Health", test_pipeline_health),
        ("System Info", test_system_info),
        ("Model Creator Endpoints", test_model_creator_endpoints),
        ("RAG Endpoints", test_rag_endpoints),
        ("Agent Creator Endpoints", test_agent_creator_endpoints),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Unified API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the service logs for details.")

    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
