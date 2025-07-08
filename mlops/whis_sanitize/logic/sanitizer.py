"""
Whis Sanitizer - Cleans, structures, and tags data like a pro data scientist.
"""

import json
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import yaml


class WhisSanitizer:
    """Main sanitizer class for processing input data."""

    def __init__(self):
        self.pii_patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
            "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        }

        self.domain_keywords = {
            "kubernetes": [
                "k8s",
                "pod",
                "deployment",
                "service",
                "namespace",
                "helm",
                "chart",
            ],
            "docker": [
                "container",
                "image",
                "dockerfile",
                "docker-compose",
                "registry",
            ],
            "mlops": [
                "ml",
                "machine learning",
                "model",
                "training",
                "inference",
                "pipeline",
            ],
            "devops": ["ci/cd", "jenkins", "gitlab", "github actions", "deployment"],
            "security": ["vulnerability", "scan", "audit", "compliance", "encryption"],
            "infrastructure": ["terraform", "ansible", "cloud", "aws", "azure", "gcp"],
        }

    def sanitize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main sanitization pipeline.

        Args:
            raw_data: Raw input data from whis_data_input

        Returns:
            Sanitized and structured data
        """
        try:
            # Generate unique ID for this processing run
            processing_id = str(uuid.uuid4())

            # Extract basic info
            content = raw_data.get("content", "")
            data_type = raw_data.get("type", "unknown")

            # Step 1: Remove PII
            sanitized_content = self._remove_pii(content)

            # Step 2: Normalize format
            normalized_content = self._normalize_format(
                sanitized_content, raw_data.get("format_hint")
            )

            # Step 3: Auto-tag
            auto_tags = self._generate_auto_tags(normalized_content, data_type)

            # Step 4: Structure data
            structured_data = self._structure_data(normalized_content, data_type)

            # Step 5: Generate metadata
            metadata = self._generate_metadata(raw_data, processing_id)

            # Prepare final output
            sanitized_data = {
                "id": processing_id,
                "original_id": raw_data.get("id"),
                "type": data_type,
                "sanitized_content": sanitized_content,
                "normalized_content": normalized_content,
                "structured_data": structured_data,
                "tags": list(set(raw_data.get("tags", []) + auto_tags)),
                "source": raw_data.get("source", "unknown"),
                "timestamp": datetime.utcnow().isoformat(),
                "status": "sanitized",
                "metadata": metadata,
                "processing_stats": {
                    "original_length": len(content),
                    "sanitized_length": len(sanitized_content),
                    "pii_removed": len(content) - len(sanitized_content),
                    "tags_generated": len(auto_tags),
                },
            }

            return sanitized_data

        except Exception as e:
            return {
                "id": str(uuid.uuid4()),
                "original_id": raw_data.get("id"),
                "type": raw_data.get("type", "unknown"),
                "status": "sanitization_failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    def _remove_pii(self, content: str) -> str:
        """Remove personally identifiable information."""
        sanitized = content

        for pii_type, pattern in self.pii_patterns.items():
            sanitized = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", sanitized)

        return sanitized

    def _normalize_format(self, content: str, format_hint: Optional[str] = None) -> str:
        """Normalize input formats to standard structure."""
        if not format_hint:
            format_hint = self._detect_format(content)

        try:
            if format_hint == "json":
                # Parse and pretty-print JSON
                parsed = json.loads(content)
                return json.dumps(parsed, indent=2)

            elif format_hint == "yaml":
                # Parse and pretty-print YAML
                parsed = yaml.safe_load(content)
                return yaml.dump(parsed, default_flow_style=False, indent=2)

            elif format_hint == "code":
                # Clean up code formatting
                return self._normalize_code(content)

            else:
                # Text content - basic cleanup
                return self._normalize_text(content)

        except Exception:
            # If parsing fails, return original content
            return content

    def _detect_format(self, content: str) -> str:
        """Auto-detect content format."""
        content = content.strip()

        # Check for JSON
        try:
            json.loads(content)
            return "json"
        except:
            pass

        # Check for YAML
        if content.startswith("---") or ("\n" in content and ":" in content):
            try:
                yaml.safe_load(content)
                return "yaml"
            except:
                pass

        # Check for code
        if any(
            marker in content
            for marker in ["```", "def ", "class ", "import ", "function "]
        ):
            return "code"

        # Default to text
        return "text"

    def _normalize_code(self, content: str) -> str:
        """Normalize code formatting."""
        # Remove extra whitespace
        lines = content.split("\n")
        normalized_lines = []

        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            if line:  # Keep non-empty lines
                normalized_lines.append(line)

        return "\n".join(normalized_lines)

    def _normalize_text(self, content: str) -> str:
        """Normalize text content."""
        # Remove extra whitespace
        content = re.sub(r"\s+", " ", content)
        # Remove extra newlines
        content = re.sub(r"\n\s*\n", "\n\n", content)
        return content.strip()

    def _generate_auto_tags(self, content: str, data_type: str) -> List[str]:
        """Generate automatic tags based on content analysis."""
        tags = [data_type]
        content_lower = content.lower()

        # Domain-specific tagging
        for domain, keywords in self.domain_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(domain)

        # Format-specific tagging
        if "json" in content_lower or "{" in content and "}" in content:
            tags.append("json")
        if "yaml" in content_lower or "---" in content:
            tags.append("yaml")
        if any(
            code_word in content_lower
            for code_word in ["def ", "class ", "import ", "function "]
        ):
            tags.append("code")

        # Language detection (basic)
        if any(word in content_lower for word in ["python", "pip", "requirements"]):
            tags.append("python")
        if any(word in content_lower for word in ["javascript", "node", "npm"]):
            tags.append("javascript")
        if any(word in content_lower for word in ["bash", "shell", "sh"]):
            tags.append("bash")

        return list(set(tags))

    def _structure_data(self, content: str, data_type: str) -> Dict[str, Any]:
        """Structure the data for downstream processing."""
        structured = {
            "raw_content": content,
            "content_type": data_type,
            "extracted_entities": self._extract_entities(content),
            "key_phrases": self._extract_key_phrases(content),
            "complexity_score": self._calculate_complexity(content),
        }

        # Add type-specific structuring
        if data_type == "qna":
            structured.update(self._structure_qna(content))
        elif data_type == "youtube_transcript":
            structured.update(self._structure_transcript(content))
        elif data_type == "info_dump":
            structured.update(self._structure_info_dump(content))

        return structured

    def _extract_entities(self, content: str) -> List[str]:
        """Extract key entities from content."""
        # Simple entity extraction (can be enhanced with NLP)
        entities = []

        # Extract URLs
        urls = re.findall(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            content,
        )
        entities.extend(urls)

        # Extract file paths
        paths = re.findall(r"[\w\-\./]+\.(?:py|js|yaml|yml|json|md|txt)", content)
        entities.extend(paths)

        # Extract command patterns
        commands = re.findall(r"(?:kubectl|docker|helm|terraform|git)\s+\w+", content)
        entities.extend(commands)

        return list(set(entities))

    def _extract_key_phrases(self, content: str) -> List[str]:
        """Extract key phrases from content."""
        # Simple key phrase extraction
        phrases = []

        # Look for technical terms
        tech_terms = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", content)
        phrases.extend([term for term in tech_terms if len(term.split()) <= 3])

        return list(set(phrases))[:10]  # Limit to top 10

    def _calculate_complexity(self, content: str) -> float:
        """Calculate content complexity score (0-1)."""
        # Simple complexity calculation
        lines = content.split("\n")
        words = content.split()

        if not words:
            return 0.0

        # Factors: line length, word count, special characters
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        word_count = len(words)
        special_chars = len(re.findall(r"[^a-zA-Z0-9\s]", content))

        # Normalize factors
        complexity = (
            min(avg_line_length / 100, 1.0) * 0.3
            + min(word_count / 1000, 1.0) * 0.3
            + min(special_chars / 500, 1.0) * 0.4
        )

        return min(complexity, 1.0)

    def _structure_qna(self, content: str) -> Dict[str, Any]:
        """Structure Q&A data."""
        return {
            "qa_type": "question_answer",
            "has_context": "context" in content.lower(),
            "question_count": content.lower().count("?"),
            "answer_indicators": len(
                re.findall(r"\b(answer|solution|fix|resolve)\b", content.lower())
            ),
        }

    def _structure_transcript(self, content: str) -> Dict[str, Any]:
        """Structure transcript data."""
        return {
            "transcript_type": "video_transcript",
            "speaker_count": len(
                re.findall(r"\b(speaker|narrator|host)\b", content.lower())
            ),
            "timestamp_count": len(re.findall(r"\d{1,2}:\d{2}", content)),
            "paragraph_count": len(content.split("\n\n")),
        }

    def _structure_info_dump(self, content: str) -> Dict[str, Any]:
        """Structure info dump data."""
        return {
            "dump_type": "information_dump",
            "code_block_count": content.count("```"),
            "url_count": len(re.findall(r"http[s]?://", content)),
            "command_count": len(re.findall(r"\$ [^\n]+", content)),
        }

    def _generate_metadata(
        self, raw_data: Dict[str, Any], processing_id: str
    ) -> Dict[str, Any]:
        """Generate processing metadata."""
        return {
            "processing_id": processing_id,
            "original_timestamp": raw_data.get("timestamp"),
            "source_service": "whis_sanitize",
            "processing_version": "1.0.0",
            "sanitization_rules_applied": list(self.pii_patterns.keys()),
            "format_detection_used": True,
            "auto_tagging_applied": True,
        }


# Convenience functions for external use
def sanitize_input(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for sanitizing input data."""
    sanitizer = WhisSanitizer()
    return sanitizer.sanitize_data(raw_data)


def batch_sanitize(raw_data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sanitize multiple inputs in batch."""
    sanitizer = WhisSanitizer()
    return [sanitizer.sanitize_data(data) for data in raw_data_list]
