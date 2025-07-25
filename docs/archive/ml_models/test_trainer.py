#!/usr/bin/env python3
"""
Test script for trainer.py
Creates sample data and tests the training functionality
"""

import json
import os
import subprocess
import tempfile

import pandas as pd


def create_sample_data():
    """Create sample property maintenance data for testing."""

    # Sample data for property maintenance
    data = {
        "property_id": range(1, 101),
        "property_type": ["apartment", "house", "condo"] * 33 + ["apartment"],
        "age_years": [5, 10, 15, 20, 25] * 20,
        "square_feet": [800, 1200, 1500, 2000, 2500] * 20,
        "contractor": [
            "Contractor A",
            "Contractor B",
            "Contractor C",
            "Contractor D",
            "Contractor E",
        ]
        * 20,
        "maintenance_type": ["plumbing", "electrical", "hvac", "roofing", "general"]
        * 20,
        "completion_time": [2, 3, 4, 5, 6] * 20,
        "cost": [500, 750, 1000, 1250, 1500] * 20,
        "quality_score": [8, 7, 9, 6, 8] * 20,
        "monthly_cost": [150, 200, 250, 300, 350] * 20,
    }

    df = pd.DataFrame(data)

    # Add some realistic variations
    import random

    random.seed(42)

    # Add noise to make it more realistic
    df["monthly_cost"] += random.randint(-50, 50)
    df["completion_time"] += random.uniform(-0.5, 0.5)
    df["cost"] += random.randint(-100, 100)
    df["quality_score"] += random.uniform(-1, 1)

    # Ensure reasonable bounds
    df["monthly_cost"] = df["monthly_cost"].clip(100, 500)
    df["completion_time"] = df["completion_time"].clip(1, 10)
    df["cost"] = df["cost"].clip(200, 2000)
    df["quality_score"] = df["quality_score"].clip(1, 10)

    return df


def test_trainer():
    """Test the trainer.py script with sample data."""

    print("🧪 Testing trainer.py...")

    # Create sample data
    df = create_sample_data()

    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        df.to_csv(f.name, index=False)
        csv_path = f.name

    try:
        # Test command
        command = [
            "python3",
            "ml_models/trainer.py",
            "--model",
            "test_maintenance_predictor",
            "--target",
            "monthly_cost",
            "--features",
            "age_years,square_feet,completion_time,cost,quality_score",
            "--data",
            csv_path,
        ]

        print(f"Running command: {' '.join(command)}")

        # Run the trainer
        result = subprocess.run(
            command, capture_output=True, text=True, cwd=os.getcwd()
        )

        print("STDOUT:")
        print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ Trainer test passed!")

            # Check if files were created
            model_path = "ml_models/models/test_maintenance_predictor.pkl"
            summary_path = "ml_models/models/test_maintenance_predictor_summary.json"

            if os.path.exists(model_path):
                print(f"✅ Model file created: {model_path}")
            else:
                print(f"❌ Model file not found: {model_path}")

            if os.path.exists(summary_path):
                print(f"✅ Summary file created: {summary_path}")

                # Read and display summary
                with open(summary_path) as f:
                    summary = json.load(f)

                print("\n📊 Training Summary:")
                print(f"  Model: {summary['model']}")
                print(f"  Target: {summary['target_column']}")
                print(f"  Features: {summary['features']}")
                print(f"  MAE: {summary['mae']:.2f}")
                print(f"  R²: {summary['r2']:.2f}")

                if "contractor_recommendations" in summary:
                    print(
                        f"  Contractor Recommendations: {len(summary['contractor_recommendations'])} contractors"
                    )
                    for i, contractor in enumerate(
                        summary["contractor_recommendations"][:3]
                    ):
                        print(
                            f"    {i+1}. {contractor['contractor']} (Score: {contractor.get('quality_score', 'N/A')})"
                        )
            else:
                print(f"❌ Summary file not found: {summary_path}")
        else:
            print(f"❌ Trainer test failed with return code: {result.returncode}")

    finally:
        # Clean up temporary file
        os.unlink(csv_path)


if __name__ == "__main__":
    test_trainer()
