from datetime import datetime
from typing import Dict, List

import pandas as pd


def format_workorder(row) -> str:
    """Format a work order row into a natural language description."""
    return f"""
    Work Order {row["workorder_id"]}: {row["work_type"].upper()} maintenance in Unit {row["unit"]}.
    Vendor: {row["vendor"]}
    Performance Metrics:
    - Response Time: {row["response_time"]} days
    - Quality Rating: {row["quality"]}/5 stars
    - Cost: ${row["cost"]}
    Date Completed: {row["date"]}
    """


def load_property_management_docs() -> List[Dict]:
    """Load and format property management data for RAG embedding."""
    try:
        # Read work orders
        df = pd.read_csv("db/fake_data/workorders.csv")

        # Generate vendor performance summaries
        vendor_stats = {}
        for vendor in df["vendor"].unique():
            vendor_data = df[df["vendor"] == vendor]
            vendor_stats[vendor] = {
                "avg_quality": vendor_data["quality"].mean(),
                "avg_response": vendor_data["response_time"].mean(),
                "avg_cost": vendor_data["cost"].mean(),
                "total_jobs": len(vendor_data),
            }

        # Create documents for embedding
        docs = []

        # Individual work order documents
        for _, row in df.iterrows():
            docs.append(
                {
                    "content": format_workorder(row),
                    "source": "workorders.csv",
                    "type": "work_order",
                    "timestamp": datetime.strptime(row["date"], "%Y-%m-%d"),
                }
            )

        # Vendor summary documents
        for vendor, stats in vendor_stats.items():
            summary = f"""
            Vendor Performance Summary: {vendor}
            Total Work Orders: {stats["total_jobs"]}
            Average Metrics:
            - Quality Rating: {stats["avg_quality"]:.1f}/5
            - Response Time: {stats["avg_response"]:.1f} days
            - Cost: ${stats["avg_cost"]:.2f}
            """
            docs.append(
                {
                    "content": summary,
                    "source": "vendor_summaries.txt",
                    "type": "vendor_summary",
                    "timestamp": datetime.now(),
                }
            )

        return docs

    except Exception as e:
        print(f"Error loading property management data: {str(e)}")
        return []


if __name__ == "__main__":
    # Test the loader
    docs = load_property_management_docs()
    print(f"Loaded {len(docs)} documents")
    print("\nSample document:")
    print(docs[0]["content"] if docs else "No documents loaded")
