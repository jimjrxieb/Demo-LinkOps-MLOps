#!/usr/bin/env python3
"""
Delinquency CSV Embedder
========================

Converts delinquency CSV files into searchable vector documents for RAG system.
Specialized for ZRS Property Management demo data.
"""

import csv
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from logic.embed import DocumentEmbedder
from logic.search import RAGSearchEngine

logger = logging.getLogger(__name__)


class DelinquencyEmbedder:
    """CSV to Vector Embedder for delinquency data."""

    def __init__(self, search_engine: Optional[RAGSearchEngine] = None):
        self.search_engine = search_engine or RAGSearchEngine()
        self.document_embedder = DocumentEmbedder()
        self.processed_files = set()

        logger.info("🔄 Delinquency Embedder initialized")

    def parse_csv_to_documents(self, csv_path: Path) -> list[dict]:
        """Parse CSV file and convert to structured documents."""
        try:
            documents = []

            with open(csv_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
                    try:
                        # Create structured content
                        content = self._create_delinquency_content(row)

                        # Create metadata
                        metadata = self._create_delinquency_metadata(row, csv_path)

                        documents.append(
                            {
                                "content": content,
                                "metadata": metadata,
                                "row_number": row_num,
                            }
                        )

                    except Exception as e:
                        logger.warning(f"⚠️ Row {row_num}: Parse error - {e}")
                        continue

            logger.info(
                f"📄 Parsed {len(documents)} delinquency records from {csv_path.name}"
            )
            return documents

        except Exception as e:
            logger.error(f"❌ CSV parsing failed for {csv_path.name}: {e}")
            return []

    def _create_delinquency_content(self, row: dict) -> str:
        """Create structured content for delinquency record."""
        # Format amount as currency
        amount_due = row.get("amount_due", "N/A")
        if amount_due and amount_due != "N/A":
            try:
                amount_formatted = f"${float(amount_due):,.2f}"
            except (ValueError, TypeError):
                amount_formatted = amount_due
        else:
            amount_formatted = amount_due

        content = f"""Delinquency Record:
- Name: {row.get("name", "N/A")}
- Amount Due: {amount_formatted}
- Property Address: {row.get("property_address", "N/A")}
- Due Date: {row.get("due_date", "N/A")}
- Status: {row.get("status", "N/A")}

This delinquency record contains information about overdue payments and property details."""

        return content

    def _create_delinquency_metadata(self, row: dict, csv_path: Path) -> dict:
        """Create metadata for delinquency record."""
        # Calculate days overdue
        days_overdue = None
        due_date = row.get("due_date")
        if due_date:
            try:
                due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
                days_overdue = (datetime.now() - due_date_obj).days
            except (ValueError, TypeError):
                days_overdue = None

        # Parse amount
        amount_due = self._parse_amount(row.get("amount_due"))

        metadata = {
            "source": csv_path.name,
            "source_type": "delinquency_csv",
            "name": row.get("name", ""),
            "amount_due": amount_due,
            "property_address": row.get("property_address", ""),
            "due_date": row.get("due_date", ""),
            "status": row.get("status", ""),
            "days_overdue": days_overdue,
            "embedded_at": datetime.now().isoformat(),
            "file_hash": self._calculate_file_hash(csv_path),
        }

        return metadata

    def _parse_amount(self, amount_str: str) -> Optional[float]:
        """Parse amount string to float."""
        try:
            if not amount_str:
                return None

            # Remove currency symbols and commas
            cleaned = amount_str.replace("$", "").replace(",", "").strip()
            return float(cleaned) if cleaned else None

        except ValueError:
            return None

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file content."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate file hash: {e}")
            return ""

    def embed_csv_file(self, csv_path: Path) -> bool:
        """Embed CSV file into vector store."""
        try:
            # Check if file was already processed
            file_hash = self._calculate_file_hash(csv_path)
            if file_hash in self.processed_files:
                logger.info(f"📄 File {csv_path.name} already processed, skipping")
                return True

            # Parse CSV to documents
            documents = self.parse_csv_to_documents(csv_path)
            if not documents:
                logger.warning(f"⚠️ No documents parsed from {csv_path.name}")
                return False

            # Extract content and metadata
            contents = [doc["content"] for doc in documents]
            metadata_list = [doc["metadata"] for doc in documents]

            # Add to search engine
            self.search_engine.add_documents(
                contents, metadata_list[0] if metadata_list else None
            )

            # Mark as processed
            self.processed_files.add(file_hash)

            logger.info(
                f"✅ Successfully embedded {len(documents)} records from {csv_path.name}"
            )
            return True

        except Exception as e:
            logger.error(f"❌ Failed to embed CSV file {csv_path.name}: {e}")
            return False

    def get_embedded_delinquencies(self) -> list[dict]:
        """Get all embedded delinquency records."""
        try:
            return self.search_engine.list_documents()
        except Exception as e:
            logger.error(f"Failed to get embedded delinquencies: {e}")
            return []

    def search_delinquencies(self, query: str, top_k: int = 5) -> list[dict]:
        """Search delinquency records."""
        try:
            results = self.search_engine.search(query, top_k=top_k)
            return [
                {
                    "content": result.content,
                    "similarity_score": result.similarity_score,
                    "metadata": result.metadata,
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Failed to search delinquencies: {e}")
            return []


def get_delinquency_embedder() -> DelinquencyEmbedder:
    """Get a delinquency embedder instance."""
    return DelinquencyEmbedder()


def embed_delinquency_csv(csv_path: Path) -> bool:
    """Embed delinquency CSV file."""
    embedder = get_delinquency_embedder()
    return embedder.embed_csv_file(csv_path)
