#!/usr/bin/env python3
"""
Test script for Whis Loopback Logic.
Tests the loopback refinement functionality.
"""

import asyncio
import json

from logic.loopback import (
    find_matching_rune,
    get_loopback_statistics,
    load_failed_tasks,
    load_repeat_tasks,
    loopback_refine,
)
from logic.version_control import get_version_history, save_version


async def test_loopback_functionality():
    """Test the complete loopback functionality."""
    print("🧪 Testing Whis Loopback Logic...")

    # Test 1: Load repeat tasks
    print("\n1. Testing repeat task loading...")
    repeat_tasks = load_repeat_tasks(threshold=2)
    print(f"   Found {len(repeat_tasks)} repeated tasks")

    # Test 2: Load failed tasks
    print("\n2. Testing failed task loading...")
    failed_tasks = load_failed_tasks()
    print(f"   Found {len(failed_tasks)} failed tasks")

    # Test 3: Test rune matching
    print("\n3. Testing rune matching...")
    sample_runes = [
        {
            "id": "test_rune_1",
            "description": "Deploy Kubernetes application",
            "keywords": ["kubernetes", "deploy", "k8s"],
        },
        {
            "id": "test_rune_2",
            "description": "Database backup",
            "keywords": ["database", "backup", "postgres"],
        },
    ]

    test_task = "Deploy a new Kubernetes application to production"
    matching_rune = find_matching_rune(test_task, sample_runes)
    if matching_rune:
        print(f"   Found matching rune: {matching_rune['id']}")
    else:
        print("   No matching rune found")

    # Test 4: Test version control
    print("\n4. Testing version control...")
    test_rune = {
        "id": "test_version_rune",
        "description": "Test rune for versioning",
        "version": 1,
    }

    try:
        version_id = save_version("runes", "test_version_rune", test_rune)
        print(f"   Saved version: {version_id}")

        history = get_version_history("runes", "test_version_rune")
        print(f"   Version history: {len(history)} versions")
    except Exception as e:
        print(f"   Version control test failed: {str(e)}")

    # Test 5: Test loopback statistics
    print("\n5. Testing loopback statistics...")
    stats = get_loopback_statistics()
    print(f"   Statistics: {json.dumps(stats, indent=2)}")

    # Test 6: Test full loopback refinement (if data exists)
    print("\n6. Testing full loopback refinement...")
    try:
        results = await loopback_refine(threshold=1)
        print(f"   Loopback results: {json.dumps(results, indent=2)}")
    except Exception as e:
        print(f"   Loopback refinement test failed: {str(e)}")

    print("\n✅ Loopback functionality tests completed!")


def test_api_endpoints():
    """Test the API endpoints."""
    print("\n🌐 Testing API endpoints...")

    import requests

    base_url = "http://localhost:8006"  # whis_enhance service port

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health endpoint error: {str(e)}")

    # Test loopback stats endpoint
    try:
        response = requests.get(f"{base_url}/loopback/stats", timeout=5)
        if response.status_code == 200:
            print("   ✅ Loopback stats endpoint working")
            stats = response.json()
            print(f"   📊 Stats: {stats}")
        else:
            print(f"   ❌ Loopback stats endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Loopback stats endpoint error: {str(e)}")

    # Test loopback trigger endpoint
    try:
        response = requests.post(f"{base_url}/loopback?threshold=1", timeout=30)
        if response.status_code == 200:
            print("   ✅ Loopback trigger endpoint working")
            result = response.json()
            print(f"   🔄 Loopback result: {result}")
        else:
            print(f"   ❌ Loopback trigger endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Loopback trigger endpoint error: {str(e)}")


if __name__ == "__main__":
    print("🚀 Starting Whis Loopback Tests...")

    # Run async tests
    asyncio.run(test_loopback_functionality())

    # Run API tests
    test_api_endpoints()

    print("\n🎉 All tests completed!")
