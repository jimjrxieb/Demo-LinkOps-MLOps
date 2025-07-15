#!/usr/bin/env python3
"""
Orb Library Management Script
Helps manage and validate the DevSecOps Orb library.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Path to the Orb library JSON file
ORB_LIBRARY_PATH = Path(__file__).parent.parent / "mlops" / "mlops-platform" / "data" / "orb_library.json"

def load_orb_library() -> List[Dict[str, Any]]:
    """Load the Orb library from JSON file."""
    try:
        with open(ORB_LIBRARY_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Orb library file not found: {ORB_LIBRARY_PATH}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in Orb library file: {e}")
        return []

def save_orb_library(orbs: List[Dict[str, Any]]) -> bool:
    """Save the Orb library to JSON file."""
    try:
        with open(ORB_LIBRARY_PATH, 'w') as f:
            json.dump(orbs, f, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving Orb library: {e}")
        return False

def validate_orb(orb: Dict[str, Any]) -> List[str]:
    """Validate a single Orb entry."""
    errors = []
    required_fields = ["title", "keywords", "orb", "rune", "confidence", "category"]
    
    for field in required_fields:
        if field not in orb:
            errors.append(f"Missing required field: {field}")
    
    if "title" in orb and not isinstance(orb["title"], str):
        errors.append("Title must be a string")
    
    if "keywords" in orb and not isinstance(orb["keywords"], list):
        errors.append("Keywords must be a list")
    
    if "confidence" in orb:
        try:
            confidence = float(orb["confidence"])
            if not (0 <= confidence <= 1):
                errors.append("Confidence must be between 0 and 1")
        except (ValueError, TypeError):
            errors.append("Confidence must be a number")
    
    return errors

def list_orbs(orbs: List[Dict[str, Any]], show_details: bool = False):
    """List all Orbs in the library."""
    print(f"📚 Orb Library ({len(orbs)} Orbs)")
    print("=" * 50)
    
    for i, orb in enumerate(orbs, 1):
        print(f"{i:2d}. {orb.get('title', 'No title')}")
        print(f"    Category: {orb.get('category', 'Unknown')}")
        print(f"    Rune: {orb.get('rune', 'No rune')}")
        print(f"    Confidence: {orb.get('confidence', 0):.2f}")
        
        if show_details:
            print(f"    Keywords: {', '.join(orb.get('keywords', []))}")
            print(f"    Orb: {orb.get('orb', 'No orb content')}")
            print()
        else:
            print()

def search_orbs(orbs: List[Dict[str, Any]], query: str):
    """Search Orbs by title, keywords, or category."""
    query_lower = query.lower()
    results = []
    
    for orb in orbs:
        title_match = query_lower in orb.get('title', '').lower()
        category_match = query_lower in orb.get('category', '').lower()
        keyword_match = any(query_lower in keyword.lower() for keyword in orb.get('keywords', []))
        
        if title_match or category_match or keyword_match:
            results.append(orb)
    
    if results:
        print(f"🔍 Search results for '{query}' ({len(results)} matches):")
        print("=" * 50)
        list_orbs(results, show_details=True)
    else:
        print(f"❌ No Orbs found matching '{query}'")

def validate_library(orbs: List[Dict[str, Any]]) -> bool:
    """Validate the entire Orb library."""
    print("🔍 Validating Orb library...")
    print("=" * 50)
    
    all_valid = True
    for i, orb in enumerate(orbs, 1):
        errors = validate_orb(orb)
        if errors:
            print(f"❌ Orb {i} ({orb.get('title', 'No title')}):")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
        else:
            print(f"✅ Orb {i}: {orb.get('title', 'No title')}")
    
    if all_valid:
        print("\n🎉 All Orbs are valid!")
    else:
        print("\n⚠️  Some Orbs have validation errors.")
    
    return all_valid

def show_stats(orbs: List[Dict[str, Any]]):
    """Show statistics about the Orb library."""
    print("📊 Orb Library Statistics")
    print("=" * 50)
    
    categories = {}
    total_keywords = 0
    
    for orb in orbs:
        category = orb.get('category', 'Unknown')
        categories[category] = categories.get(category, 0) + 1
        total_keywords += len(orb.get('keywords', []))
    
    print(f"Total Orbs: {len(orbs)}")
    print(f"Total Keywords: {total_keywords}")
    print(f"Average Keywords per Orb: {total_keywords / len(orbs):.1f}" if orbs else "N/A")
    print(f"Categories: {len(categories)}")
    print()
    
    print("Categories:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} Orbs")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python manage-orb-library.py <command> [options]")
        print("\nCommands:")
        print("  list              - List all Orbs")
        print("  list --details    - List all Orbs with full details")
        print("  search <query>    - Search Orbs by title, keywords, or category")
        print("  validate          - Validate all Orbs")
        print("  stats             - Show library statistics")
        print("  test              - Test loading and validation")
        return
    
    command = sys.argv[1]
    orbs = load_orb_library()
    
    if not orbs:
        print("❌ No Orbs loaded. Check the JSON file.")
        return
    
    if command == "list":
        show_details = "--details" in sys.argv
        list_orbs(orbs, show_details)
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Please provide a search query")
            return
        query = " ".join(sys.argv[2:])
        search_orbs(orbs, query)
    
    elif command == "validate":
        validate_library(orbs)
    
    elif command == "stats":
        show_stats(orbs)
    
    elif command == "test":
        print("🧪 Testing Orb library...")
        print(f"✅ Loaded {len(orbs)} Orbs from {ORB_LIBRARY_PATH}")
        print(f"✅ JSON is valid")
        is_valid = validate_library(orbs)
        if is_valid:
            print("✅ All tests passed!")
        else:
            print("❌ Validation tests failed!")
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main() 