#!/usr/bin/env python3
"""
Test Script for Upload and Q&A Functionality
============================================

This script tests the drag-and-drop upload and local RAG Q&A functionality.
"""

import time
from pathlib import Path

import requests

# Configuration
RAG_BASE_URL = "http://localhost:8005"
TEST_FILE_PATH = "sample_data/kubernetes_basics.txt"


def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{RAG_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_upload_file():
    """Test file upload functionality."""
    print("\n📤 Testing file upload...")

    if not Path(TEST_FILE_PATH).exists():
        print(f"❌ Test file not found: {TEST_FILE_PATH}")
        return False

    try:
        with open(TEST_FILE_PATH, "rb") as f:
            files = {"file": (Path(TEST_FILE_PATH).name, f, "text/plain")}
            response = requests.post(f"{RAG_BASE_URL}/upload", files=files)

        if response.status_code == 200:
            result = response.json()
            print(f"✅ File uploaded successfully: {result['filename']}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False


def test_query():
    """Test Q&A functionality."""
    print("\n❓ Testing Q&A query...")

    query_data = {
        "query": "What is Kubernetes?",
        "top_k": 3,
        "similarity_threshold": 0.5,
        "include_metadata": True,
    }

    try:
        response = requests.post(f"{RAG_BASE_URL}/query-simple", json=query_data)

        if response.status_code == 200:
            result = response.json()
            print("✅ Query successful")
            print(f"   Answer: {result['answer'][:100]}...")
            print(f"   Execution time: {result['execution_time']:.2f}s")
            print(f"   Results: {result['total_results']}")
            return True
        else:
            print(f"❌ Query failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False


def test_documents_list():
    """Test documents listing."""
    print("\n📋 Testing documents list...")

    try:
        response = requests.get(f"{RAG_BASE_URL}/documents")

        if response.status_code == 200:
            result = response.json()
            print("✅ Documents listed successfully")
            print(f"   Total documents: {result['total_documents']}")
            return True
        else:
            print(f"❌ Documents list failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Documents list error: {e}")
        return False


def test_stats():
    """Test statistics endpoint."""
    print("\n📊 Testing statistics...")

    try:
        response = requests.get(f"{RAG_BASE_URL}/stats")

        if response.status_code == 200:
            result = response.json()
            print("✅ Statistics retrieved")
            print(f"   Documents: {result['total_documents']}")
            print(f"   Chunks: {result['total_chunks']}")
            print(f"   Vector store size: {result['vectorstore_size_mb']:.2f} MB")
            return True
        else:
            print(f"❌ Statistics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Statistics error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing Upload and Q&A Functionality")
    print("=" * 50)

    tests = [
        test_health_check,
        test_upload_file,
        test_query,
        test_documents_list,
        test_stats,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Small delay between tests

    print("\n" + "=" * 50)
    print(f"📈 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print(
            "🎉 All tests passed! The upload and Q&A functionality is working correctly."
        )
    else:
        print("⚠️ Some tests failed. Check the RAG service and try again.")

    return passed == total


if __name__ == "__main__":
    main()
