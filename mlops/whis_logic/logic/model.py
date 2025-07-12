"""
Whis Logic - Whis's internal ML model brain for embedding generation and similarity search.
"""

import shlex
from datetime import datetime
from typing import Any, Dict, List

import numpy as np


def sanitize_cmd(cmd):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    if not isinstance(cmd, list) or not cmd:
        raise ValueError("Invalid command passed to sanitize_cmd()")
    allowed = {
        "ls",
        "echo",
        "kubectl",
        "helm",
        "python3",
        "cat",
        "go",
        "docker",
        "npm",
        "black",
        "ruff",
        "yamllint",
        "prettier",
        "flake8",
    }
    if cmd[0] not in allowed:
        raise ValueError(f"Blocked dangerous command: {cmd[0]}")
    return cmd


class WhisLogic:
    """Whis's internal ML model brain."""

    def __init__(self):
        self.embeddings_cache = {}
        self.similarity_threshold = 0.8

    def generate_embedding(
        self, content: str, content_type: str = "text"
    ) -> List[float]:
        """
        Generate embedding for content.

        Args:
            content: Input content
            content_type: Type of content (text, code, yaml, etc.)

        Returns:
            Embedding vector
        """
        # TODO: Implement actual embedding generation
        # For now, return mock embedding
        embedding = np.random.rand(384).tolist()  # 384-dimensional embedding

        # Cache the embedding
        content_hash = hash(content)
        self.embeddings_cache[content_hash] = {
            "embedding": embedding,
            "content_type": content_type,
            "timestamp": datetime.utcnow().isoformat(),
        }

        return embedding

    def calculate_similarity(
        self, embedding1: List[float], embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score (0-1)
        """
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Calculate cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        return float(similarity)

    def find_similar_content(
        self,
        query_embedding: List[float],
        content_embeddings: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Find similar content based on embeddings.

        Args:
            query_embedding: Query embedding
            content_embeddings: List of content with embeddings
            top_k: Number of top results to return

        Returns:
            List of similar content with similarity scores
        """
        similarities = []

        for content in content_embeddings:
            content_embedding = content.get("embedding", [])
            if content_embedding:
                similarity = self.calculate_similarity(
                    query_embedding, content_embedding
                )
                similarities.append({**content, "similarity_score": similarity})

        # Sort by similarity score (descending)
        similarities.sort(key=lambda x: x["similarity_score"], reverse=True)

        # Filter by threshold and return top_k
        filtered_results = [
            result
            for result in similarities
            if result["similarity_score"] >= self.similarity_threshold
        ]

        return filtered_results[:top_k]

    def generate_recommendations(
        self, user_context: Dict[str, Any], available_assets: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on user context.

        Args:
            user_context: User's current context
            available_assets: Available orbs and runes

        Returns:
            List of recommended assets
        """
        # Generate embedding for user context
        context_text = self._extract_context_text(user_context)
        context_embedding = self.generate_embedding(context_text)

        # Prepare asset embeddings
        asset_embeddings = []
        for asset in available_assets:
            asset_text = self._extract_asset_text(asset)
            asset_embedding = self.generate_embedding(asset_text)
            asset_embeddings.append({**asset, "embedding": asset_embedding})

        # Find similar assets
        similar_assets = self.find_similar_content(
            context_embedding, asset_embeddings, top_k=10
        )

        # Add recommendation metadata
        recommendations = []
        for i, asset in enumerate(similar_assets):
            recommendation = {
                **asset,
                "recommendation_rank": i + 1,
                "recommendation_reason": self._generate_recommendation_reason(
                    asset, user_context
                ),
                "confidence_score": asset.get("similarity_score", 0.0),
            }
            recommendations.append(recommendation)

        return recommendations

    def _extract_context_text(self, user_context: Dict[str, Any]) -> str:
        """Extract text from user context for embedding generation."""
        context_parts = []

        if "current_task" in user_context:
            context_parts.append(user_context["current_task"])

        if "recent_activities" in user_context:
            for activity in user_context["recent_activities"]:
                context_parts.append(str(activity))

        if "tags" in user_context:
            context_parts.extend(user_context["tags"])

        return " ".join(context_parts)

    def _extract_asset_text(self, asset: Dict[str, Any]) -> str:
        """Extract text from asset for embedding generation."""
        asset_parts = []

        if "title" in asset:
            asset_parts.append(asset["title"])

        if "content" in asset:
            if isinstance(asset["content"], dict):
                # Handle structured content
                for key, value in asset["content"].items():
                    if isinstance(value, str):
                        asset_parts.append(value)
                    elif isinstance(value, list):
                        asset_parts.extend([str(item) for item in value])
            else:
                asset_parts.append(str(asset["content"]))

        if "tags" in asset:
            asset_parts.extend(asset["tags"])

        return " ".join(asset_parts)

    def _generate_recommendation_reason(
        self, asset: Dict[str, Any], user_context: Dict[str, Any]
    ) -> str:
        """Generate human-readable reason for recommendation."""
        asset_type = asset.get("type", "unknown")
        similarity_score = asset.get("similarity_score", 0.0)

        if asset_type == "orb":
            return f"Best practice orb with {similarity_score:.1%} relevance to your current task"
        elif asset_type == "rune":
            return f"Automation rune with {similarity_score:.1%} match to your workflow"
        else:
            return f"Asset with {similarity_score:.1%} similarity to your context"


# Convenience functions for external use
def generate_embedding(content: str, content_type: str = "text") -> List[float]:
    """Generate embedding for content."""
    logic = WhisLogic()
    return logic.generate_embedding(content, content_type)


def find_similar_content(
    query_embedding: List[float],
    content_embeddings: List[Dict[str, Any]],
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """Find similar content based on embeddings."""
    logic = WhisLogic()
    return logic.find_similar_content(query_embedding, content_embeddings, top_k)


def generate_recommendations(
    user_context: Dict[str, Any], available_assets: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Generate recommendations based on user context."""
    logic = WhisLogic()
    return logic.generate_recommendations(user_context, available_assets)
