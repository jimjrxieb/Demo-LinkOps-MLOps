#!/usr/bin/env python3
"""
Test script for Orb scoring functionality
"""

import sys
from pathlib import Path

# Add the ficknury-evaluator to the path
sys.path.append(str(Path(__file__).parent.parent / "shadows" / "ficknury-evaluator"))

try:
    from orb_scoring import get_library_stats, score_task_against_orbs, search_orbs

    print("🧪 Testing Orb Scoring Functionality")
    print("=" * 50)

    # Test 1: Library stats
    print("\n1. 📊 Library Statistics:")
    stats = get_library_stats()
    print(f"   Total Orbs: {stats['total_orbs']}")
    print(f"   Categories: {stats['category_count']}")
    print(f"   Categories: {list(stats['categories'].keys())}")

    # Test 2: Search functionality
    print("\n2. 🔍 Search Test:")
    search_results = search_orbs("security")
    print(f"   Found {len(search_results)} Orbs matching 'security'")
    for orb in search_results[:3]:  # Show first 3
        print(f"   - {orb['title']} ({orb['category']})")

    # Test 3: Task scoring
    print("\n3. 🎯 Task Scoring Test:")
    test_tasks = [
        "scan container images for vulnerabilities",
        "implement CI/CD pipeline linting",
        "set up Kubernetes pod security policies",
        "random task that shouldn't match anything",
    ]

    for task in test_tasks:
        result = score_task_against_orbs(task)
        print(f"\n   Task: '{task}'")
        print(f"   Automatable: {result['automatable']}")
        if result["best_match"]:
            print(f"   Best match: {result['best_match']['orb']['title']}")
            print(f"   Score: {result['best_match']['score']:.2f}")
            print(f"   Category: {result['best_match']['category']}")
        else:
            print(f"   Best match: None")

    print("\n✅ All tests completed successfully!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the DEMO-LinkOps directory")
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback

    traceback.print_exc()
