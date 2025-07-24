#!/usr/bin/env python3
"""
RAG Service Test Suite
=====================

Test the RAG service functionality.
"""

import json
import time
from pathlib import Path

import requests

# RAG service configuration
RAG_BASE_URL = "http://localhost:8005"


def test_health_endpoint():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")

    try:
        response = requests.get(f"{RAG_BASE_URL}/health", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Vector store status: {data['vectorstore_status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_embed_document():
    """Test document embedding."""
    print("\n📄 Testing document embedding...")

    # Create test document
    test_content = """
    The zero trust model is a security framework that requires all users to be authenticated and authorized before accessing any resources.
    
    Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.
    
    Docker is a platform for developing, shipping, and running applications in containers.
    
    Kubernetes is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.
    """

    test_file = "/tmp/test_document.txt"
    with open(test_file, "w") as f:
        f.write(test_content)

    try:
        # Test embedding
        embed_data = {
            "file_path": test_file,
            "chunk_size": 200,
            "chunk_overlap": 50,
            "metadata": {"source": "test", "author": "test_user", "version": "1.0"},
        }

        response = requests.post(f"{RAG_BASE_URL}/embed/", json=embed_data, timeout=30)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Document embedded successfully")
            print(f"   Chunks created: {data['embedding_stats']['chunks_created']}")
            print(f"   Processing time: {data['execution_time']:.2f}s")
            return True
        else:
            print(f"❌ Embedding failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return False


def test_search_query():
    """Test search functionality."""
    print("\n🔍 Testing search functionality...")

    try:
        # Test search
        search_data = {
            "query": "What is zero trust?",
            "top_k": 3,
            "similarity_threshold": 0.5,
            "include_metadata": True,
        }

        response = requests.post(f"{RAG_BASE_URL}/query/", json=search_data, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search completed successfully")
            print(f"   Query: {data['query']}")
            print(f"   Results found: {data['total_results']}")
            print(f"   Execution time: {data['execution_time']:.3f}s")

            # Show results
            for i, result in enumerate(data["results"], 1):
                print(f"\n   Result {i}:")
                print(f"     Score: {result['similarity_score']:.3f}")
                print(f"     Content: {result['content'][:100]}...")

            return True
        else:
            print(f"❌ Search failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Search error: {e}")
        return False


def test_simple_search():
    """Test simple search endpoint."""
    print("\n🔍 Testing simple search...")

    try:
        response = requests.get(
            f"{RAG_BASE_URL}/search/",
            params={
                "query": "machine learning",
                "top_k": 2,
                "similarity_threshold": 0.3,
            },
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Simple search completed")
            print(f"   Results found: {data['total_results']}")
            return True
        else:
            print(f"❌ Simple search failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Simple search error: {e}")
        return False


def test_list_documents():
    """Test document listing."""
    print("\n📋 Testing document listing...")

    try:
        response = requests.get(f"{RAG_BASE_URL}/documents/", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Document listing completed")
            print(f"   Total documents: {data['total_documents']}")

            for doc in data["documents"]:
                print(f"   - {doc['document_id']}: {doc['chunks_count']} chunks")

            return True
        else:
            print(f"❌ Document listing failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Document listing error: {e}")
        return False


def test_system_stats():
    """Test system statistics."""
    print("\n📊 Testing system statistics...")

    try:
        response = requests.get(f"{RAG_BASE_URL}/stats/", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ System stats retrieved")
            print(f"   Total documents: {data['total_documents']}")
            print(f"   Total chunks: {data['total_chunks']}")
            print(f"   Vector store size: {data['vectorstore_size_mb']:.2f}MB")
            print(f"   Embedding model: {data['embedding_model']}")
            print(f"   Index type: {data['index_type']}")
            return True
        else:
            print(f"❌ System stats failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ System stats error: {e}")
        return False


def test_available_models():
    """Test available models endpoint."""
    print("\n🤖 Testing available models...")

    try:
        response = requests.get(f"{RAG_BASE_URL}/models/", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available models retrieved")
            print(f"   Current model: {data['current_model']}")
            print(f"   Available models: {len(data['available_models'])}")
            return True
        else:
            print(f"❌ Available models failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Available models error: {e}")
        return False


def test_reload_index():
    """Test index reload."""
    print("\n🔄 Testing index reload...")

    try:
        response = requests.post(f"{RAG_BASE_URL}/reload/", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Index reload completed: {data['message']}")
            return True
        else:
            print(f"❌ Index reload failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Index reload error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 RAG Service Test Suite")
    print("=" * 40)

    # Wait for service to be ready
    print("⏳ Waiting for RAG service to be ready...")
    time.sleep(5)

    # Run tests
    tests = [
        ("Health Check", test_health_endpoint),
        ("Document Embedding", test_embed_document),
        ("Search Query", test_search_query),
        ("Simple Search", test_simple_search),
        ("List Documents", test_list_documents),
        ("System Stats", test_system_stats),
        ("Available Models", test_available_models),
        ("Reload Index", test_reload_index),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n📋 Test Summary")
    print("=" * 40)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the service logs for details.")


if __name__ == "__main__":
    main()
