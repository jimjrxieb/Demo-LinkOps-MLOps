"""
FickNury Evaluator - Orb Scoring Module
Scores tasks against the DevSecOps Orb library for automation path evaluation
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Load the Orb Library
ORB_PATH = Path(__file__).parent / "data" / "orb_library.json"

try:
    with open(ORB_PATH) as f:
        orb_library = json.load(f)
    logger.info(f"✅ Loaded {len(orb_library)} Orbs from {ORB_PATH}")
except FileNotFoundError:
    logger.warning(f"❌ Orb library file not found: {ORB_PATH}")
    orb_library = []
except json.JSONDecodeError as e:
    logger.error(f"❌ Invalid JSON in Orb library file: {e}")
    orb_library = []


class OrbScorer:
    """Scores tasks against the DevSecOps Orb library"""

    def __init__(self):
        self.orb_library = orb_library
        self.categories = self._extract_categories()

    def _extract_categories(self) -> List[str]:
        """Extract unique categories from the Orb library"""
        categories = set()
        for orb in self.orb_library:
            categories.add(orb.get("category", "Unknown"))
        return sorted(list(categories))

    def score_task_against_orbs(self, task: str) -> Dict[str, Any]:
        """
        Score a task against all Orbs in the library

        Args:
            task: Task description to score

        Returns:
            Scoring results with best matches and recommendations
        """
        task_lower = task.lower()
        matches = []

        for orb in self.orb_library:
            score = self._calculate_orb_score(task_lower, orb)
            if score > 0:
                matches.append(
                    {
                        "orb": orb,
                        "score": score,
                        "confidence": orb.get("confidence", 0.0),
                        "category": orb.get("category", "Unknown"),
                        "rune": orb.get("rune", "Unknown"),
                    }
                )

        # Sort by score (highest first)
        matches.sort(key=lambda x: x["score"], reverse=True)

        # Determine if task is automatable
        best_match = matches[0] if matches else None
        automatable = best_match is not None and best_match["score"] >= 0.3

        return {
            "task": task,
            "automatable": automatable,
            "best_match": best_match,
            "all_matches": matches,
            "total_matches": len(matches),
            "recommendation": self._generate_recommendation(best_match, task),
            "category_breakdown": self._get_category_breakdown(matches),
            "scored_at": "{{datetime.now().isoformat()}}",
        }

    def _calculate_orb_score(self, task_lower: str, orb: Dict[str, Any]) -> float:
        """
        Calculate how well a task matches an Orb

        Args:
            task_lower: Lowercase task description
            orb: Orb definition from library

        Returns:
            Score between 0.0 and 1.0
        """
        keywords = orb.get("keywords", [])
        if not keywords:
            return 0.0

        # Count keyword matches
        keyword_matches = sum(
            1 for keyword in keywords if keyword.lower() in task_lower
        )

        # Calculate base score
        base_score = keyword_matches / len(keywords)

        # Boost score for title matches
        title = orb.get("title", "").lower()
        if any(word in task_lower for word in title.split()):
            base_score += 0.2

        # Boost score for category relevance
        category = orb.get("category", "").lower()
        if category in task_lower:
            base_score += 0.1

        return min(base_score, 1.0)

    def _generate_recommendation(
        self, best_match: Optional[Dict[str, Any]], task: str
    ) -> Dict[str, Any]:
        """Generate recommendation based on best match"""
        if not best_match:
            return {
                "action": "manual_review",
                "reason": "No matching Orbs found in library",
                "suggestions": [
                    "Review task requirements",
                    "Consider breaking down into smaller tasks",
                    "Check if task fits existing categories",
                ],
            }

        orb = best_match["orb"]
        score = best_match["score"]

        if score >= 0.7:
            return {
                "action": "automate",
                "reason": f"High confidence match with {orb.get('title', 'Orb')}",
                "confidence": score,
                "rune": orb.get("rune", "Unknown"),
                "implementation": orb.get("orb", "No implementation details"),
            }
        elif score >= 0.4:
            return {
                "action": "semi_automate",
                "reason": f"Moderate match with {orb.get('title', 'Orb')} - may need adaptation",
                "confidence": score,
                "rune": orb.get("rune", "Unknown"),
                "implementation": orb.get("orb", "No implementation details"),
                "notes": "Consider manual review before automation",
            }
        else:
            return {
                "action": "manual_review",
                "reason": f"Low confidence match with {orb.get('title', 'Orb')}",
                "confidence": score,
                "suggestions": [
                    "Review task requirements",
                    "Consider manual execution",
                    "Check for similar Orbs",
                ],
            }

    def _get_category_breakdown(self, matches: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get breakdown of matches by category"""
        breakdown = {}
        for match in matches:
            category = match["category"]
            breakdown[category] = breakdown.get(category, 0) + 1
        return breakdown

    def search_orbs(self, query: str) -> List[Dict[str, Any]]:
        """
        Search Orbs by title, keywords, or category

        Args:
            query: Search query

        Returns:
            List of matching Orbs
        """
        query_lower = query.lower()
        results = []

        for orb in self.orb_library:
            title_match = query_lower in orb.get("title", "").lower()
            category_match = query_lower in orb.get("category", "").lower()
            keyword_match = any(
                query_lower in keyword.lower() for keyword in orb.get("keywords", [])
            )

            if title_match or category_match or keyword_match:
                results.append(orb)

        return results

    def get_orb_by_rune(self, rune: str) -> Optional[Dict[str, Any]]:
        """Get Orb by its rune identifier"""
        for orb in self.orb_library:
            if orb.get("rune") == rune:
                return orb
        return None

    def get_orbs_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all Orbs in a specific category"""
        return [orb for orb in self.orb_library if orb.get("category") == category]

    def get_library_stats(self) -> Dict[str, Any]:
        """Get statistics about the Orb library"""
        categories = {}
        total_keywords = 0

        for orb in self.orb_library:
            category = orb.get("category", "Unknown")
            categories[category] = categories.get(category, 0) + 1
            total_keywords += len(orb.get("keywords", []))

        return {
            "total_orbs": len(self.orb_library),
            "total_keywords": total_keywords,
            "average_keywords_per_orb": (
                total_keywords / len(self.orb_library) if self.orb_library else 0
            ),
            "categories": categories,
            "category_count": len(categories),
        }


# Global instance for easy access
orb_scorer = OrbScorer()


def score_task_against_orbs(task: str) -> Dict[str, Any]:
    """
    Convenience function to score a task against Orbs

    Args:
        task: Task description to score

    Returns:
        Scoring results
    """
    return orb_scorer.score_task_against_orbs(task)


def search_orbs(query: str) -> List[Dict[str, Any]]:
    """
    Convenience function to search Orbs

    Args:
        query: Search query

    Returns:
        List of matching Orbs
    """
    return orb_scorer.search_orbs(query)


def get_library_stats() -> Dict[str, Any]:
    """
    Convenience function to get library statistics

    Returns:
        Library statistics
    """
    return orb_scorer.get_library_stats()
