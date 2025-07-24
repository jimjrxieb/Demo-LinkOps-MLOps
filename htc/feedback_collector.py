#!/usr/bin/env python3
"""
HTC Feedback Collector
=====================

Collects user feedback and corrections for AI answers to enable local model retraining.
This creates a closed-loop system for continuous improvement of the RAG system.
"""

import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Configuration
LOG_DIR = Path("htc/feedback/")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Feedback categories
FEEDBACK_CATEGORIES = [
    "incorrect_answer",
    "incomplete_answer",
    "wrong_context",
    "missing_information",
    "unclear_response",
    "other",
]


class FeedbackCollector:
    """Collects and manages feedback for AI answer improvements."""

    def __init__(self, log_dir: Path = LOG_DIR):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📝 Feedback collector initialized: {self.log_dir}")

    def log_feedback(
        self,
        query: str,
        generated_answer: str,
        expected_answer: str,
        context: str = "",
        source: Optional[str] = None,
        category: str = "incorrect_answer",
        user_notes: str = "",
        tenant_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Log feedback for an AI answer correction.

        Args:
            query: Original user question
            generated_answer: AI-generated answer that needs correction
            expected_answer: Correct answer provided by user
            context: Context used to generate the answer
            source: Source of the query (e.g., "tenant_csv", "document")
            category: Type of feedback issue
            user_notes: Additional notes from user
            tenant_data: Related tenant information if applicable

        Returns:
            Dictionary with feedback entry details
        """
        try:
            # Generate unique ID for this feedback
            timestamp = datetime.now()
            feedback_id = self._generate_feedback_id(query, timestamp)

            # Create feedback entry
            entry = {
                "feedback_id": feedback_id,
                "timestamp": timestamp.isoformat(),
                "query": query,
                "generated_answer": generated_answer,
                "expected_answer": expected_answer,
                "context": context,
                "source": source,
                "category": category,
                "user_notes": user_notes,
                "tenant_data": tenant_data or {},
                "status": "pending_training",
                "training_round": 0,
            }

            # Save to file
            file_path = self.log_dir / f"{feedback_id}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Feedback logged: {feedback_id}")
            logger.info(f"   Query: {query[:50]}...")
            logger.info(f"   Category: {category}")

            return entry

        except Exception as e:
            logger.error(f"❌ Failed to log feedback: {e}")
            raise

    def _generate_feedback_id(self, query: str, timestamp: datetime) -> str:
        """Generate unique feedback ID."""
        # Create hash from query and timestamp
        content = f"{query}_{timestamp.isoformat()}"
        hash_obj = hashlib.md5(content.encode())
        return (
            f"feedback_{timestamp.strftime('%Y%m%d_%H%M%S')}_{hash_obj.hexdigest()[:8]}"
        )

    def get_feedback_entries(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent feedback entries."""
        try:
            entries = []
            files = sorted(
                self.log_dir.glob("*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )

            for file_path in files[:limit]:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        entry = json.load(f)
                        entries.append(entry)
                except Exception as e:
                    logger.warning(f"Failed to read feedback file {file_path}: {e}")
                    continue

            return entries

        except Exception as e:
            logger.error(f"Failed to get feedback entries: {e}")
            return []

    def get_feedback_by_id(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        """Get specific feedback entry by ID."""
        try:
            file_path = self.log_dir / f"{feedback_id}.json"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to get feedback {feedback_id}: {e}")
            return None

    def update_feedback_status(
        self, feedback_id: str, status: str, training_round: int = 0
    ) -> bool:
        """Update feedback status after training."""
        try:
            file_path = self.log_dir / f"{feedback_id}.json"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    entry = json.load(f)

                entry["status"] = status
                entry["training_round"] = training_round
                entry["last_updated"] = datetime.now().isoformat()

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(entry, f, indent=2, ensure_ascii=False)

                logger.info(f"✅ Updated feedback status: {feedback_id} -> {status}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to update feedback status: {e}")
            return False

    def get_feedback_stats(self) -> Dict[str, Any]:
        """Get feedback statistics."""
        try:
            entries = self.get_feedback_entries(limit=1000)  # Get all entries

            stats = {
                "total_feedback": len(entries),
                "categories": {},
                "status": {},
                "recent_feedback": len(
                    [e for e in entries if self._is_recent(e, days=7)]
                ),
                "pending_training": len(
                    [e for e in entries if e.get("status") == "pending_training"]
                ),
                "trained": len([e for e in entries if e.get("status") == "trained"]),
            }

            # Count by category
            for entry in entries:
                category = entry.get("category", "unknown")
                stats["categories"][category] = stats["categories"].get(category, 0) + 1

                status = entry.get("status", "unknown")
                stats["status"][status] = stats["status"].get(status, 0) + 1

            return stats

        except Exception as e:
            logger.error(f"Failed to get feedback stats: {e}")
            return {"total_feedback": 0, "error": str(e)}

    def _is_recent(self, entry: Dict[str, Any], days: int = 7) -> bool:
        """Check if feedback entry is recent."""
        try:
            timestamp = datetime.fromisoformat(entry.get("timestamp", ""))
            days_ago = datetime.now().timestamp() - (days * 24 * 60 * 60)
            return timestamp.timestamp() > days_ago
        except:
            return False

    def build_training_dataset(self) -> str:
        """
        Build training dataset from feedback entries.

        Returns:
            Path to the generated training file
        """
        try:
            entries = self.get_feedback_entries(limit=1000)
            training_data = []

            for entry in entries:
                # Create training prompt
                prompt = self._create_training_prompt(entry)
                training_data.append(prompt)

            # Save training dataset
            training_file = self.log_dir / "training_dataset.txt"
            with open(training_file, "w", encoding="utf-8") as f:
                f.write("\n\n".join(training_data))

            logger.info(f"✅ Training dataset created: {len(training_data)} examples")
            return str(training_file)

        except Exception as e:
            logger.error(f"Failed to build training dataset: {e}")
            raise

    def _create_training_prompt(self, entry: Dict[str, Any]) -> str:
        """Create training prompt from feedback entry."""
        query = entry.get("query", "")
        context = entry.get("context", "")
        expected_answer = entry.get("expected_answer", "")

        # Format for instruction tuning
        prompt = f"""### Question: {query}

### Context: {context}

### Correct Answer: {expected_answer}

### End"""

        return prompt

    def cleanup_old_feedback(self, days: int = 90) -> int:
        """Clean up old feedback entries."""
        try:
            count = 0
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

            for file_path in self.log_dir.glob("*.json"):
                try:
                    if file_path.stat().st_mtime < cutoff_time:
                        file_path.unlink()
                        count += 1
                except Exception as e:
                    logger.warning(f"Failed to delete old feedback {file_path}: {e}")

            logger.info(f"🗑️ Cleaned up {count} old feedback entries")
            return count

        except Exception as e:
            logger.error(f"Failed to cleanup old feedback: {e}")
            return 0


# Global instance
_feedback_collector = None


def get_feedback_collector() -> FeedbackCollector:
    """Get global feedback collector instance."""
    global _feedback_collector
    if _feedback_collector is None:
        _feedback_collector = FeedbackCollector()
    return _feedback_collector


def log_feedback(
    query: str,
    answer: str,
    expected: str,
    context: str = "",
    source: Optional[str] = None,
    category: str = "incorrect_answer",
    user_notes: str = "",
    tenant_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Convenience function to log feedback."""
    collector = get_feedback_collector()
    return collector.log_feedback(
        query=query,
        generated_answer=answer,
        expected_answer=expected,
        context=context,
        source=source,
        category=category,
        user_notes=user_notes,
        tenant_data=tenant_data,
    )


if __name__ == "__main__":
    # Test the feedback collector
    collector = FeedbackCollector()

    # Test logging feedback
    test_feedback = log_feedback(
        query="When is rent due?",
        answer="Rent is due on the 1st of each month.",
        expected="Rent is due on the 1st of each month, with a 5-day grace period.",
        context="Tenant lease agreement",
        source="tenant_csv",
        category="incomplete_answer",
        user_notes="Missing grace period information",
    )

    print("✅ Test feedback logged:", test_feedback["feedback_id"])

    # Test getting feedback
    entries = collector.get_feedback_entries(limit=5)
    print(f"📝 Found {len(entries)} feedback entries")

    # Test stats
    stats = collector.get_feedback_stats()
    print("📊 Feedback stats:", stats)
