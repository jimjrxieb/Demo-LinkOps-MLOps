#!/usr/bin/env python3
"""
HTC Prompt Template Builder
===========================

Builds custom prompt templates from domain-specific terms and variations.
This enables property managers to customize how the AI understands their terminology.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Configuration
PROMPT_DIR = Path("prompts")
PROMPT_FILE = PROMPT_DIR / "query_rewrite_prompt.txt"
TERMS_FILE = Path("htc/prompt_terms.json")

# Ensure directories exist
PROMPT_DIR.mkdir(parents=True, exist_ok=True)
TERMS_FILE.parent.mkdir(parents=True, exist_ok=True)


class TermVariation:
    """Represents a domain term and its variations."""

    def __init__(
        self,
        term: str,
        variations: List[str],
        category: str = "other",
        description: str = "",
    ):
        self.term = term
        self.variations = variations
        self.category = category
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "term": self.term,
            "variations": self.variations,
            "category": self.category,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TermVariation":
        """Create from dictionary."""
        return cls(
            term=data.get("term", ""),
            variations=data.get("variations", []),
            category=data.get("category", "other"),
            description=data.get("description", ""),
        )


def build_prompt_from_terms(terms: List[TermVariation]) -> str:
    """
    Build prompt template from custom terms.

    Args:
        terms: List of domain terms and their variations

    Returns:
        Generated prompt template
    """
    prompt_lines = [
        "You are an AI assistant helping generate diverse rephrasings of a user's question to improve document retrieval from a property management knowledge base.",
        "",
        "🔄 Use these known term variations:",
    ]

    # Add term variations
    for term in terms:
        if term.variations:
            variations_str = ", ".join(term.variations)
            prompt_lines.append(f'- "{term.term}" → {variations_str}')

    # Add instructions
    prompt_lines.extend(
        [
            "",
            "When rephrasing a query, generate 4 alternate versions using synonyms or domain-aware variations.",
            "Focus on property management terminology and common variations.",
            "Consider the context and intent of the original question.",
            "",
            "Format:",
            "User Question: {question}",
            "",
            "Alternate Rephrasings:",
            "1.",
            "2.",
            "3.",
            "4.",
        ]
    )

    return "\n".join(prompt_lines)


def build_enhanced_prompt_from_terms(terms: List[TermVariation]) -> str:
    """
    Build enhanced prompt template with more detailed instructions.

    Args:
        terms: List of domain terms and their variations

    Returns:
        Enhanced prompt template
    """
    prompt_lines = [
        "You are an AI assistant specialized in property management query understanding and rephrasing.",
        "Your goal is to generate diverse, semantically equivalent rephrasings of user questions to improve document retrieval.",
        "",
        "🔄 Domain-Specific Term Variations:",
    ]

    # Group terms by category
    categories = {}
    for term in terms:
        if term.category not in categories:
            categories[term.category] = []
        categories[term.category].append(term)

    # Add terms by category
    for category, category_terms in categories.items():
        if category != "other":
            category_name = category.replace("_", " ").title()
            prompt_lines.append(f"\n📂 {category_name}:")
            for term in category_terms:
                if term.variations:
                    variations_str = ", ".join(term.variations)
                    prompt_lines.append(f'  - "{term.term}" → {variations_str}')

    # Add other terms
    if "other" in categories:
        prompt_lines.append(f"\n📂 Other Terms:")
        for term in categories["other"]:
            if term.variations:
                variations_str = ", ".join(term.variations)
                prompt_lines.append(f'  - "{term.term}" → {variations_str}')

    # Add detailed instructions
    prompt_lines.extend(
        [
            "",
            "🎯 Rephrasing Guidelines:",
            "1. Use domain-specific synonyms and variations",
            "2. Maintain the original intent and context",
            "3. Consider different ways users might phrase the same question",
            "4. Include both formal and informal variations",
            "5. Account for regional or company-specific terminology",
            "",
            "📝 Output Format:",
            "User Question: {question}",
            "",
            "Alternate Rephrasings:",
            "1. [First variation using domain terms]",
            "2. [Second variation with different synonyms]",
            "3. [Third variation with alternative phrasing]",
            "4. [Fourth variation considering context]",
        ]
    )

    return "\n".join(prompt_lines)


def save_terms_to_file(
    terms: List[TermVariation], file_path: Path = TERMS_FILE
) -> bool:
    """
    Save terms to JSON file.

    Args:
        terms: List of terms to save
        file_path: Path to save the terms

    Returns:
        True if successful, False otherwise
    """
    try:
        terms_data = [term.to_dict() for term in terms]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(terms_data, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Terms saved to {file_path}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to save terms: {e}")
        return False


def load_terms_from_file(file_path: Path = TERMS_FILE) -> List[TermVariation]:
    """
    Load terms from JSON file.

    Args:
        file_path: Path to load terms from

    Returns:
        List of loaded terms
    """
    try:
        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            terms_data = json.load(f)

        terms = [TermVariation.from_dict(term) for term in terms_data]
        logger.info(f"📖 Loaded {len(terms)} terms from {file_path}")
        return terms

    except Exception as e:
        logger.error(f"❌ Failed to load terms: {e}")
        return []


def save_prompt_template(prompt_text: str, file_path: Path = PROMPT_FILE) -> bool:
    """
    Save prompt template to file.

    Args:
        prompt_text: Prompt template content
        file_path: Path to save the prompt

    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(prompt_text)

        logger.info(f"✅ Prompt template saved to {file_path}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to save prompt template: {e}")
        return False


def load_prompt_template(file_path: Path = PROMPT_FILE) -> Optional[str]:
    """
    Load prompt template from file.

    Args:
        file_path: Path to load prompt from

    Returns:
        Prompt template content or None if not found
    """
    try:
        if not file_path.exists():
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            prompt_text = f.read()

        logger.info(f"📖 Loaded prompt template from {file_path}")
        return prompt_text

    except Exception as e:
        logger.error(f"❌ Failed to load prompt template: {e}")
        return None


def get_term_variations(file_path: Path = TERMS_FILE) -> Dict[str, List[str]]:
    """
    Get term variations for use in search.

    Args:
        file_path: Path to terms file

    Returns:
        Dictionary mapping terms to their variations
    """
    try:
        terms = load_terms_from_file(file_path)
        variations = {}

        for term in terms:
            if term.term and term.variations:
                variations[term.term] = term.variations

        return variations

    except Exception as e:
        logger.error(f"Failed to get term variations: {e}")
        return {}


def create_sample_terms() -> List[TermVariation]:
    """
    Create sample property management terms for demonstration.

    Returns:
        List of sample terms
    """
    sample_terms = [
        TermVariation(
            term="delinquency",
            variations=[
                "late rent",
                "rent not paid",
                "overdue payment",
                "payment delinquency",
                "past due",
            ],
            category="rent_payment",
            description="Terms related to unpaid or late rent",
        ),
        TermVariation(
            term="eviction",
            variations=[
                "lease termination",
                "notice to vacate",
                "removal",
                "expulsion",
                "legal removal",
            ],
            category="legal",
            description="Terms related to tenant removal from property",
        ),
        TermVariation(
            term="lease renewal",
            variations=[
                "contract extension",
                "lease extension",
                "renewal",
                "extend lease",
                "continue lease",
            ],
            category="lease_management",
            description="Terms related to extending existing leases",
        ),
        TermVariation(
            term="maintenance request",
            variations=[
                "repair request",
                "service request",
                "work order",
                "fix request",
                "maintenance ticket",
            ],
            category="maintenance",
            description="Terms related to property maintenance and repairs",
        ),
        TermVariation(
            term="security deposit",
            variations=[
                "deposit",
                "damage deposit",
                "bond",
                "security bond",
                "rental deposit",
            ],
            category="financial",
            description="Terms related to security deposits and bonds",
        ),
    ]

    return sample_terms


def validate_terms(terms: List[TermVariation]) -> List[str]:
    """
    Validate terms for errors.

    Args:
        terms: List of terms to validate

    Returns:
        List of validation errors
    """
    errors = []

    for i, term in enumerate(terms):
        # Check term name
        if not term.term or not term.term.strip():
            errors.append(f"Term {i+1}: Term name is required")
        elif len(term.term.strip()) < 2:
            errors.append(f"Term {i+1}: Term name must be at least 2 characters")

        # Check variations
        if not term.variations:
            errors.append(f"Term {i+1}: At least one variation is required")
        elif len(term.variations) > 10:
            errors.append(f"Term {i+1}: Maximum 10 variations allowed")
        else:
            # Check individual variations
            for j, variation in enumerate(term.variations):
                if not variation or not variation.strip():
                    errors.append(
                        f"Term {i+1}, Variation {j+1}: Variation cannot be empty"
                    )
                elif len(variation.strip()) < 2:
                    errors.append(
                        f"Term {i+1}, Variation {j+1}: Variation must be at least 2 characters"
                    )

    return errors


def get_terms_statistics(terms: List[TermVariation]) -> Dict[str, Any]:
    """
    Get statistics about terms.

    Args:
        terms: List of terms to analyze

    Returns:
        Dictionary with statistics
    """
    stats = {
        "total_terms": len(terms),
        "total_variations": sum(len(term.variations) for term in terms),
        "categories": {},
        "avg_variations_per_term": 0,
    }

    # Count by category
    for term in terms:
        category = term.category
        stats["categories"][category] = stats["categories"].get(category, 0) + 1

    # Calculate average variations
    if stats["total_terms"] > 0:
        stats["avg_variations_per_term"] = (
            stats["total_variations"] / stats["total_terms"]
        )

    return stats


if __name__ == "__main__":
    # Test the prompt template builder
    print("🧠 HTC Prompt Template Builder Test")
    print("=" * 50)

    # Create sample terms
    sample_terms = create_sample_terms()
    print(f"📝 Created {len(sample_terms)} sample terms")

    # Build prompt
    prompt = build_prompt_from_terms(sample_terms)
    print(f"📄 Generated prompt template ({len(prompt)} characters)")

    # Save to file
    if save_terms_to_file(sample_terms):
        print("✅ Sample terms saved")

    if save_prompt_template(prompt):
        print("✅ Prompt template saved")

    # Load and verify
    loaded_terms = load_terms_from_file()
    print(f"📖 Loaded {len(loaded_terms)} terms")

    loaded_prompt = load_prompt_template()
    print(
        f"📖 Loaded prompt template ({len(loaded_prompt) if loaded_prompt else 0} characters)"
    )

    # Get statistics
    stats = get_terms_statistics(sample_terms)
    print(f"📊 Statistics: {stats}")

    print("\n🎉 Test completed successfully!")
