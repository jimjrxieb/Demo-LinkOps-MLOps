#!/usr/bin/env python3
"""
CSV Embedder for Tenant Data
============================

Converts tenant CSV files into searchable vector documents for RAG system.
Integrates with existing vector store and search engine.
"""

import csv
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from logic.embed import DocumentEmbedder

# Import existing RAG components
from logic.search import RAGSearchEngine

logger = logging.getLogger(__name__)


class CSVTEmbedder:
    """CSV to Vector Embedder for tenant data."""

    def __init__(self, search_engine: Optional[RAGSearchEngine] = None):
        self.search_engine = search_engine or RAGSearchEngine()
        self.document_embedder = DocumentEmbedder()
        self.processed_files = set()

        logger.info("🔄 CSV Embedder initialized")

    def parse_csv_to_documents(self, csv_path: Path) -> list[dict]:
        """Parse CSV file and convert to structured documents."""
        try:
            documents = []

            with open(csv_path, encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
                    try:
                        # Create structured content
                        content = self._create_tenant_content(row)

                        # Create metadata
                        metadata = self._create_tenant_metadata(row, csv_path)

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
                f"📄 Parsed {len(documents)} tenant records from {csv_path.name}"
            )
            return documents

        except Exception as e:
            logger.error(f"❌ CSV parsing failed for {csv_path.name}: {e}")
            return []

    def _create_tenant_content(self, row: dict) -> str:
        """Create structured content for tenant record."""
        # Format dates nicely
        lease_start = row.get("lease_start", "N/A")
        lease_end = row.get("lease_end", "N/A")
        rent_amount = row.get("rent_amount", "N/A")

        # Format rent as currency if it's a number
        if rent_amount and rent_amount != "N/A":
            try:
                rent_formatted = f"${float(rent_amount):,.2f}"
            except (ValueError, TypeError):
                rent_formatted = rent_amount
        else:
            rent_formatted = rent_amount

        content = f"""Tenant Record:
- Name: {row.get("tenant_name", "N/A")}
- Unit: {row.get("unit", "N/A")}
- Status: {row.get("status", "N/A")}
- Lease Start: {lease_start}
- Lease End: {lease_end}
- Monthly Rent: {rent_formatted}
- Email: {row.get("email", "N/A")}
- Phone: {row.get("phone", "N/A")}

This tenant record contains information about the rental unit, lease terms, and contact details."""

        return content

    def _create_tenant_metadata(self, row: dict, csv_path: Path) -> dict:
        """Create metadata for tenant record."""
        # Calculate days until lease expires
        days_until_expiry = None
        lease_end = row.get("lease_end")
        if lease_end:
            try:
                end_date = datetime.strptime(lease_end, "%Y-%m-%d")
                days_until_expiry = (end_date - datetime.now()).days
            except (ValueError, TypeError):
                days_until_expiry = None

        # Determine lease status
        lease_status = "active"
        if days_until_expiry is not None:
            if days_until_expiry < 0:
                lease_status = "expired"
            elif days_until_expiry <= 30:
                lease_status = "expiring_soon"
            elif days_until_expiry <= 90:
                lease_status = "expiring_later"

        metadata = {
            "source": csv_path.name,
            "source_type": "tenant_csv",
            "tenant_name": row.get("tenant_name", ""),
            "unit": row.get("unit", ""),
            "status": row.get("status", "active"),
            "lease_start": row.get("lease_start", ""),
            "lease_end": row.get("lease_end", ""),
            "rent_amount": self._parse_rent_amount(row.get("rent_amount")),
            "email": row.get("email", ""),
            "phone": row.get("phone", ""),
            "lease_status": lease_status,
            "days_until_expiry": days_until_expiry,
            "embedded_at": datetime.now().isoformat(),
            "file_hash": self._calculate_file_hash(csv_path),
        }

        return metadata

    def _parse_rent_amount(self, rent_str: str) -> Optional[float]:
        """Parse rent amount string to float."""
        try:
            if not rent_str:
                return None

            # Remove currency symbols and commas
            cleaned = rent_str.replace("$", "").replace(",", "").strip()
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
            logger.error(f"❌ Failed to calculate file hash: {e}")
            return ""

    def embed_csv_file(self, csv_path: Path) -> bool:
        """Embed a CSV file into the vector store."""
        try:
            logger.info(f"🔄 Embedding CSV file: {csv_path.name}")

            # Check if file already processed
            file_hash = self._calculate_file_hash(csv_path)
            if file_hash in self.processed_files:
                logger.info(f"⏭️ File already processed: {csv_path.name}")
                return True

            # Parse CSV to documents
            documents = self.parse_csv_to_documents(csv_path)
            if not documents:
                logger.warning(f"⚠️ No valid documents found in {csv_path.name}")
                return False

            # Add documents to search engine
            for doc in documents:
                self.search_engine.add_documents(
                    documents=[doc["content"]], metadata=doc["metadata"]
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

    def embed_csv_content(
        self, csv_content: str, filename: str = "uploaded.csv"
    ) -> bool:
        """Embed CSV content directly (for API uploads)."""
        try:
            # Create temporary file
            temp_path = Path(f"/tmp/{filename}")
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(csv_content)

            # Embed the file
            success = self.embed_csv_file(temp_path)

            # Clean up
            temp_path.unlink(missing_ok=True)

            return success

        except Exception as e:
            logger.error(f"❌ Failed to embed CSV content: {e}")
            return False

    def get_embedded_tenants(self) -> list[dict]:
        """Get list of embedded tenant records."""
        try:
            # This would need to be implemented based on your vector store
            # For now, return a placeholder
            return []
        except Exception as e:
            logger.error(f"❌ Failed to get embedded tenants: {e}")
            return []

    def search_tenants(self, query: str, top_k: int = 5) -> list[dict]:
        """Search tenant records using the RAG system."""
        try:
            results = self.search_engine.search(
                query=query,
                top_k=top_k,
                similarity_threshold=0.5,
                include_metadata=True,
            )

            return [
                {
                    "content": result.content,
                    "metadata": result.metadata,
                    "score": result.score,
                }
                for result in results
            ]

        except Exception as e:
            logger.error(f"❌ Failed to search tenants: {e}")
            return []


# Global instance
_csv_embedder = None


def get_csv_embedder() -> CSVTEmbedder:
    """Get global CSV embedder instance."""
    global _csv_embedder
    if _csv_embedder is None:
        _csv_embedder = CSVTEmbedder()
    return _csv_embedder


def embed_csv_file(csv_path: Path) -> bool:
    """Convenience function to embed a CSV file."""
    embedder = get_csv_embedder()
    return embedder.embed_csv_file(csv_path)


def embed_csv_content(csv_content: str, filename: str = "uploaded.csv") -> bool:
    """Convenience function to embed CSV content."""
    embedder = get_csv_embedder()
    return embedder.embed_csv_content(csv_content, filename)
