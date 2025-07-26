from datetime import datetime, timedelta
from typing import Dict, Optional

import pandas as pd


class VendorSuggestionModel:
    def __init__(self):
        self.df = pd.read_csv("db/fake_data/workorders.csv")
        self._calculate_vendor_stats()

    def _calculate_vendor_stats(self):
        """Calculate and cache vendor performance statistics."""
        self.vendor_stats = {}
        for vendor in self.df["vendor"].unique():
            vendor_data = self.df[df["vendor"] == vendor]
            self.vendor_stats[vendor] = {
                "avg_quality": vendor_data["quality"].mean(),
                "avg_response": vendor_data["response_time"].mean(),
                "avg_cost": vendor_data["cost"].mean(),
                "total_jobs": len(vendor_data),
                "last_job": pd.to_datetime(vendor_data["date"]).max(),
            }

    def _normalize_score(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize a value to a 0-1 scale."""
        return (value - min_val) / (max_val - min_val) if max_val > min_val else 0.5

    def suggest_vendor(self, work_type: str, parameters: Optional[Dict] = None) -> Dict:
        """
        Suggest the best vendor based on work type and weighted parameters.

        Args:
            work_type: Type of work needed (hvac, plumbing, electrical)
            parameters: Dict of importance weights for different factors
                - quality_weight: 0-1 importance of quality rating
                - response_weight: 0-1 importance of response time
                - cost_weight: 0-1 importance of cost
                - Default weights prioritize quality

        Returns:
            Dict containing suggested vendor and their scores
        """
        # Default parameters prioritize quality
        params = {"quality_weight": 0.5, "response_weight": 0.3, "cost_weight": 0.2}
        if parameters:
            params.update(parameters)

        # Filter by work type
        filtered = self.df[self.df["work_type"] == work_type].copy()
        if len(filtered) == 0:
            return {"error": f"No vendors found for work type: {work_type}"}

        # Calculate scores for each vendor
        vendor_scores = []
        for vendor in filtered["vendor"].unique():
            vendor_data = filtered[filtered["vendor"] == vendor]

            # Get recent performance (last 90 days)
            recent_data = vendor_data[
                pd.to_datetime(vendor_data["date"])
                >= (datetime.now() - timedelta(days=90))
            ]

            # Calculate normalized scores
            quality_score = self._normalize_score(
                vendor_data["quality"].mean(),
                filtered["quality"].min(),
                filtered["quality"].max(),
            )

            response_score = 1 - self._normalize_score(  # Invert so lower is better
                vendor_data["response_time"].mean(),
                filtered["response_time"].min(),
                filtered["response_time"].max(),
            )

            cost_score = 1 - self._normalize_score(  # Invert so lower is better
                vendor_data["cost"].mean(),
                filtered["cost"].min(),
                filtered["cost"].max(),
            )

            # Calculate weighted final score
            final_score = (
                quality_score * params["quality_weight"]
                + response_score * params["response_weight"]
                + cost_score * params["cost_weight"]
            )

            vendor_scores.append(
                {
                    "vendor": vendor,
                    "score": round(final_score * 100, 1),  # Convert to percentage
                    "metrics": {
                        "quality": round(quality_score * 100, 1),
                        "response_time": round(response_score * 100, 1),
                        "cost": round(cost_score * 100, 1),
                    },
                    "stats": {
                        "avg_quality": round(vendor_data["quality"].mean(), 1),
                        "avg_response": round(vendor_data["response_time"].mean(), 1),
                        "avg_cost": round(vendor_data["cost"].mean(), 2),
                        "total_jobs": len(vendor_data),
                        "recent_jobs": len(recent_data),
                    },
                }
            )

        # Sort by score and return top vendor
        vendor_scores.sort(key=lambda x: x["score"], reverse=True)
        return vendor_scores[0]

    def get_explanation(self, suggestion: Dict) -> str:
        """Generate a natural language explanation for the vendor suggestion."""
        vendor = suggestion["vendor"]
        stats = suggestion["stats"]
        metrics = suggestion["metrics"]

        explanation = f"""Based on analysis of {stats["total_jobs"]} work orders, {vendor} is the recommended choice:

• Quality: {stats["avg_quality"]}/5 rating ({metrics["quality"]}% percentile)
• Response: {stats["avg_response"]} days avg. ({metrics["response_time"]}% percentile)
• Cost: ${stats["avg_cost"]} avg. ({metrics["cost"]}% percentile)

They have completed {stats["recent_jobs"]} jobs in the last 90 days."""

        return explanation


if __name__ == "__main__":
    # Test the model
    model = VendorSuggestionModel()

    # Test with different parameter weights
    test_params = [
        {
            "quality_weight": 0.8,
            "response_weight": 0.1,
            "cost_weight": 0.1,
        },  # Quality focused
        {
            "quality_weight": 0.1,
            "response_weight": 0.8,
            "cost_weight": 0.1,
        },  # Speed focused
        {
            "quality_weight": 0.1,
            "response_weight": 0.1,
            "cost_weight": 0.8,
        },  # Cost focused
    ]

    for params in test_params:
        suggestion = model.suggest_vendor("hvac", params)
        print("\nTest with parameters:", params)
        print("Suggested vendor:", suggestion["vendor"])
        print("Score:", suggestion["score"])
        print("\nExplanation:")
        print(model.get_explanation(suggestion))
