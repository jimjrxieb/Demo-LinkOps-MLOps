#!/usr/bin/env python3
"""
HTC Prompt Editor API Routes
============================

FastAPI routes for managing custom AI keywords and prompt templates.
This enables property managers to customize how the AI understands their domain terminology.
"""

import json
import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()

# Configuration
PROMPT_DIR = Path("prompts")
PROMPT_FILE = PROMPT_DIR / "query_rewrite_prompt.txt"
TERMS_FILE = Path("htc/prompt_terms.json")

# Ensure directories exist
PROMPT_DIR.mkdir(parents=True, exist_ok=True)
TERMS_FILE.parent.mkdir(parents=True, exist_ok=True)


# Pydantic models
class TermVariation(BaseModel):
    term: str
    variations: list[str]
    category: str = "other"
    description: str = ""


class TermList(BaseModel):
    terms: list[TermVariation]


class PromptTemplate(BaseModel):
    template: str
    description: str = ""


@router.post("/htc/prompt/keywords")
async def update_keywords(payload: TermList):
    """
    Update custom AI keywords and generate prompt template.

    Args:
        payload: List of domain terms and their variations

    Returns:
        Success response with term count
    """
    try:
        logger.info(f"📝 Updating AI keywords: {len(payload.terms)} terms")

        # Save terms to JSON file
        terms_data = [term.dict() for term in payload.terms]
        with open(TERMS_FILE, "w", encoding="utf-8") as f:
            json.dump(terms_data, f, indent=2, ensure_ascii=False)

        # Generate prompt template from terms
        prompt_text = build_prompt_from_terms(payload.terms)

        # Save prompt template
        with open(PROMPT_FILE, "w", encoding="utf-8") as f:
            f.write(prompt_text)

        logger.info("✅ Keywords updated successfully")
        logger.info(f"   Terms saved: {TERMS_FILE}")
        logger.info(f"   Prompt generated: {PROMPT_FILE}")

        return {
            "status": "success",
            "terms_count": len(payload.terms),
            "total_variations": sum(len(term.variations) for term in payload.terms),
            "prompt_file": str(PROMPT_FILE),
            "terms_file": str(TERMS_FILE),
        }

    except Exception as e:
        logger.error(f"❌ Failed to update keywords: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to update keywords: {str(e)}"
        )


@router.get("/htc/prompt/keywords")
async def get_keywords():
    """
    Get current custom AI keywords.

    Returns:
        List of domain terms and their variations
    """
    try:
        if not TERMS_FILE.exists():
            return {"terms": []}

        with open(TERMS_FILE, encoding="utf-8") as f:
            terms_data = json.load(f)

        # Convert to TermVariation objects
        terms = [TermVariation(**term) for term in terms_data]

        logger.info(f"📖 Retrieved {len(terms)} custom keywords")
        return {"terms": [term.dict() for term in terms]}

    except Exception as e:
        logger.error(f"❌ Failed to get keywords: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get keywords: {str(e)}")


@router.get("/htc/prompt/template")
async def get_prompt_template():
    """
    Get current prompt template.

    Returns:
        Current prompt template content
    """
    try:
        if not PROMPT_FILE.exists():
            return {"template": "", "description": "No custom prompt template found"}

        with open(PROMPT_FILE, encoding="utf-8") as f:
            template_content = f.read()

        return {
            "template": template_content,
            "description": "Custom prompt template for query rewriting",
            "file_path": str(PROMPT_FILE),
        }

    except Exception as e:
        logger.error(f"❌ Failed to get prompt template: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get prompt template: {str(e)}"
        )


@router.post("/htc/prompt/template")
async def update_prompt_template(payload: PromptTemplate):
    """
    Update prompt template manually.

    Args:
        payload: New prompt template content

    Returns:
        Success response
    """
    try:
        logger.info("📝 Updating prompt template manually")

        # Save prompt template
        with open(PROMPT_FILE, "w", encoding="utf-8") as f:
            f.write(payload.template)

        logger.info(f"✅ Prompt template updated: {PROMPT_FILE}")

        return {
            "status": "success",
            "file_path": str(PROMPT_FILE),
            "template_length": len(payload.template),
        }

    except Exception as e:
        logger.error(f"❌ Failed to update prompt template: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to update prompt template: {str(e)}"
        )


@router.get("/htc/prompt/stats")
async def get_prompt_stats():
    """
    Get statistics about custom keywords and prompt template.

    Returns:
        Statistics about the prompt system
    """
    try:
        stats = {
            "terms_file_exists": TERMS_FILE.exists(),
            "prompt_file_exists": PROMPT_FILE.exists(),
            "terms_count": 0,
            "total_variations": 0,
            "categories": {},
            "prompt_length": 0,
        }

        # Get terms statistics
        if TERMS_FILE.exists():
            with open(TERMS_FILE, encoding="utf-8") as f:
                terms_data = json.load(f)

            stats["terms_count"] = len(terms_data)
            stats["total_variations"] = sum(
                len(term.get("variations", [])) for term in terms_data
            )

            # Count by category
            for term in terms_data:
                category = term.get("category", "other")
                stats["categories"][category] = stats["categories"].get(category, 0) + 1

        # Get prompt statistics
        if PROMPT_FILE.exists():
            with open(PROMPT_FILE, encoding="utf-8") as f:
                prompt_content = f.read()
            stats["prompt_length"] = len(prompt_content)

        return stats

    except Exception as e:
        logger.error(f"❌ Failed to get prompt stats: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get prompt stats: {str(e)}"
        )


@router.delete("/htc/prompt/keywords")
async def clear_keywords():
    """
    Clear all custom keywords and reset to default.

    Returns:
        Success response
    """
    try:
        logger.info("🗑️ Clearing all custom keywords")

        # Remove terms file
        if TERMS_FILE.exists():
            TERMS_FILE.unlink()

        # Remove prompt file
        if PROMPT_FILE.exists():
            PROMPT_FILE.unlink()

        logger.info("✅ All custom keywords cleared")

        return {"status": "success", "message": "All custom keywords cleared"}

    except Exception as e:
        logger.error(f"❌ Failed to clear keywords: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to clear keywords: {str(e)}"
        )


@router.get("/htc/prompt/categories")
async def get_categories():
    """
    Get available categories for organizing terms.

    Returns:
        List of available categories
    """
    categories = [
        {
            "value": "rent_payment",
            "label": "Rent Payment",
            "description": "Terms related to rent collection and payments",
        },
        {
            "value": "lease_management",
            "label": "Lease Management",
            "description": "Terms related to lease agreements and renewals",
        },
        {
            "value": "maintenance",
            "label": "Maintenance",
            "description": "Terms related to property maintenance and repairs",
        },
        {
            "value": "tenant_communication",
            "label": "Tenant Communication",
            "description": "Terms related to tenant interactions",
        },
        {
            "value": "legal",
            "label": "Legal & Compliance",
            "description": "Terms related to legal matters and compliance",
        },
        {
            "value": "financial",
            "label": "Financial",
            "description": "Terms related to financial operations and accounting",
        },
        {
            "value": "property_operations",
            "label": "Property Operations",
            "description": "Terms related to day-to-day property management",
        },
        {
            "value": "other",
            "label": "Other",
            "description": "Terms that don't fit other categories",
        },
    ]

    return {"categories": categories}


def build_prompt_from_terms(terms: list[TermVariation]) -> str:
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


def load_custom_prompt() -> Optional[str]:
    """
    Load custom prompt template if it exists.

    Returns:
        Custom prompt template or None if not found
    """
    try:
        if PROMPT_FILE.exists():
            with open(PROMPT_FILE, encoding="utf-8") as f:
                return f.read()
        return None
    except Exception as e:
        logger.error(f"Failed to load custom prompt: {e}")
        return None


def get_term_variations() -> dict[str, list[str]]:
    """
    Get term variations for use in search.

    Returns:
        Dictionary mapping terms to their variations
    """
    try:
        if not TERMS_FILE.exists():
            return {}

        with open(TERMS_FILE, encoding="utf-8") as f:
            terms_data = json.load(f)

        variations = {}
        for term in terms_data:
            term_name = term.get("term", "")
            term_variations = term.get("variations", [])
            if term_name and term_variations:
                variations[term_name] = term_variations

        return variations

    except Exception as e:
        logger.error(f"Failed to load term variations: {e}")
        return {}
