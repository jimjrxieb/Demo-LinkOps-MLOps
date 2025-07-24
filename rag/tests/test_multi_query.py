#!/usr/bin/env python3
"""
MultiQueryRetriever Test Script
==============================

Test script to validate the MultiQueryRetriever functionality for smarter tenant Q&A.
"""

import logging
import sys
from pathlib import Path

# Add the rag directory to the path
sys.path.append(str(Path(__file__).parent))

from logic.search import RAGSearchEngine, retrieve_chunks

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_multi_query_retriever():
    """Test the MultiQueryRetriever functionality."""
    print("🧠 MultiQueryRetriever Test")
    print("=" * 50)

    # Initialize search engine
    search_engine = RAGSearchEngine()

    # Check if MultiQueryRetriever is available
    if not search_engine.use_multi_query:
        print("❌ MultiQueryRetriever not available")
        print("   - Check if LLM model exists at:", search_engine.llm_model_path)
        print("   - Check if LangChain is properly installed")
        return

    print("✅ MultiQueryRetriever initialized successfully")

    # Test queries that would benefit from MultiQueryRetriever
    test_queries = [
        "When is rent considered late?",
        "Which tenants have leases ending this month?",
        "Who hasn't paid rent?",
        "What's the average rent in building A?",
        "Show me all active tenants in unit 101",
        "Which tenants are behind on payments?",
        "Who has the highest rent?",
        "Which units are currently vacant?",
        "Show me tenants with rent over $2000",
        "What's the contact info for John Smith?",
    ]

    print(f"\n🔍 Testing {len(test_queries)} queries...")
    print("-" * 50)

    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")

        try:
            # Test MultiQueryRetriever
            multi_results = search_engine.search_with_multi_query(
                query=query, top_k=3, similarity_threshold=0.5, include_metadata=True
            )

            print(f"   MultiQuery Results: {len(multi_results)} found")

            # Show top result
            if multi_results:
                top_result = multi_results[0]
                print(f"   Top Result Score: {top_result.similarity_score:.3f}")
                print(f"   Content Preview: {top_result.content[:100]}...")

                # Show metadata if available
                if top_result.metadata:
                    metadata_info = []
                    if "tenant_name" in top_result.metadata:
                        metadata_info.append(
                            f"Tenant: {top_result.metadata['tenant_name']}"
                        )
                    if "unit" in top_result.metadata:
                        metadata_info.append(f"Unit: {top_result.metadata['unit']}")
                    if "source" in top_result.metadata:
                        metadata_info.append(f"Source: {top_result.metadata['source']}")

                    if metadata_info:
                        print(f"   Metadata: {', '.join(metadata_info)}")
            else:
                print("   No results found")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("🎉 MultiQueryRetriever test completed!")


def test_retrieve_chunks_function():
    """Test the convenience retrieve_chunks function."""
    print("\n🔧 Testing retrieve_chunks convenience function")
    print("-" * 50)

    test_query = "Which tenants have leases ending this month?"
    print(f"Query: {test_query}")

    try:
        # Test with MultiQueryRetriever enabled
        results = retrieve_chunks(test_query, use_multi_query=True)
        print(f"MultiQuery Results: {len(results)} found")

        # Test with MultiQueryRetriever disabled
        results_simple = retrieve_chunks(test_query, use_multi_query=False)
        print(f"Simple Search Results: {len(results_simple)} found")

        # Compare results
        if len(results) > len(results_simple):
            print("✅ MultiQueryRetriever found more relevant results")
        elif len(results) == len(results_simple):
            print("📊 Both methods found similar number of results")
        else:
            print("⚠️ Simple search found more results")

    except Exception as e:
        print(f"❌ Error: {e}")


def test_tenant_specific_queries():
    """Test queries specifically designed for tenant data."""
    print("\n🏠 Testing Tenant-Specific Queries")
    print("-" * 50)

    tenant_queries = [
        "rent payment status",
        "lease expiration dates",
        "tenant contact information",
        "unit occupancy status",
        "monthly rent amounts",
        "tenant names and units",
        "active vs inactive tenants",
        "rent collection issues",
        "lease renewal information",
        "tenant complaints or issues",
    ]

    search_engine = RAGSearchEngine()

    for query in tenant_queries:
        print(f"\nQuery: {query}")

        try:
            results = search_engine.search_with_multi_query(
                query=query,
                top_k=2,
                similarity_threshold=0.3,  # Lower threshold for broader results
                include_metadata=True,
            )

            print(f"Results: {len(results)} found")

            if results:
                # Show if any results have tenant metadata
                tenant_results = [
                    r for r in results if r.metadata and "tenant_name" in r.metadata
                ]
                print(f"Tenant records: {len(tenant_results)}")

                if tenant_results:
                    print("Sample tenant data found:")
                    for result in tenant_results[:2]:
                        tenant_name = result.metadata.get("tenant_name", "Unknown")
                        unit = result.metadata.get("unit", "Unknown")
                        print(f"  - {tenant_name} (Unit {unit})")

        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main test function."""
    print("🧠 MultiQueryRetriever Comprehensive Test Suite")
    print("=" * 60)

    # Test 1: Basic MultiQueryRetriever functionality
    test_multi_query_retriever()

    # Test 2: Convenience function
    test_retrieve_chunks_function()

    # Test 3: Tenant-specific queries
    test_tenant_specific_queries()

    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("\n💡 MultiQueryRetriever Benefits:")
    print("   - Generates multiple semantically similar queries")
    print("   - Improves search coverage for vague questions")
    print("   - Better results for property management queries")
    print("   - Handles synonyms and variations automatically")
    print("   - Uses MMR search for diverse, relevant results")


if __name__ == "__main__":
    main()
