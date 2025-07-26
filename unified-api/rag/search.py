from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, List

import numpy as np

# Demo embedded documents for testing
DEMO_DOCS = [
    {
        "content": "Maintenance costs have increased by 12% this month, primarily due to HVAC repairs. Three units required emergency service calls.",
        "source": "maintenance_report_2024.pdf",
        "embedding": np.random.rand(384),  # Simulated embedding
        "timestamp": datetime(2024, 1, 15),
    },
    {
        "content": "Stark Repairs (Contractor ID: CR-789) has completed 8 work orders with a perfect 5/5 rating. Specializes in HVAC and electrical.",
        "source": "contractor_reviews.xlsx",
        "embedding": np.random.rand(384),
        "timestamp": datetime(2024, 1, 10),
    },
    {
        "content": "New tenant onboarding process requires credit check, background verification, and income verification (3x monthly rent).",
        "source": "tenant_policies.docx",
        "embedding": np.random.rand(384),
        "timestamp": datetime(2024, 1, 5),
    },
]


def highlight_match(text: str, query: str, window: int = 50) -> str:
    """Extract and highlight best matching snippet."""
    match = SequenceMatcher(None, text.lower(), query.lower()).find_longest_match(
        0, len(text), 0, len(query)
    )
    if match.size == 0:
        return text  # No match found, return original text

    start = max(match.a - window, 0)
    end = min(match.a + match.size + window, len(text))

    # Add ellipsis if we're not showing the full text
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""

    # Extract snippet and highlight the matched portion
    snippet = text[start:end]
    highlighted = snippet.replace(
        text[match.a : match.a + match.size],
        f"<mark>{text[match.a : match.a + match.size]}</mark>",
    )

    return f"{prefix}{highlighted}{suffix}"


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def semantic_search(query: str, top_k: int = 3) -> List[Dict]:
    """
    Perform semantic search over embedded documents.

    Args:
        query: The search query
        top_k: Number of results to return

    Returns:
        List of matching documents with similarity scores and highlights
    """
    # In production:
    # 1. Generate query embedding using same model as docs
    # 2. Load real document embeddings from vector store
    # 3. Perform approximate nearest neighbor search
    query_embedding = np.random.rand(384)  # Simulated query embedding

    results = []
    for doc in DEMO_DOCS:
        similarity = cosine_similarity(query_embedding, doc["embedding"])
        results.append(
            {
                "content": doc["content"],
                "source": doc["source"],
                "score": float(similarity),
                "timestamp": doc["timestamp"],
                "highlight": highlight_match(doc["content"], query),
            }
        )

    # Sort by similarity score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
