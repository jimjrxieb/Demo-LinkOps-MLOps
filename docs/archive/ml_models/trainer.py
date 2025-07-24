import argparse
import json
import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def recommend_contractors(df):
    """Rank contractors by performance metrics."""
    contractors = (
        df.groupby("contractor")
        .agg({"completion_time": "mean", "cost": "mean", "quality_score": "mean"})
        .reset_index()
    )

    # Lower completion_time and cost is better, higher quality_score is better
    contractors["rank_score"] = (
        -contractors["completion_time"] * 0.3
        + -contractors["cost"] * 0.3
        + contractors["quality_score"] * 0.4
    )

    contractors = contractors.sort_values(by="rank_score", ascending=False)
    return contractors[
        ["contractor", "completion_time", "cost", "quality_score"]
    ].to_dict(orient="records")


def train_model(args):
    print("🔄 Starting model training...")

    df = pd.read_csv(args.data)

    if args.target not in df.columns:
        raise ValueError(f"Target column '{args.target}' not found in CSV.")

    features = args.features.split(",")
    for f in features:
        if f not in df.columns:
            raise ValueError(f"Feature column '{f}' not found in CSV.")

    X = df[features]
    y = df[args.target]

    # Handle non-numeric categorical values
    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"✅ Model trained: MAE={mae:.2f}, R2={r2:.2f}")

    # Save model
    os.makedirs("ml_models/models", exist_ok=True)
    model_path = f"ml_models/models/{args.model}.pkl"
    joblib.dump(model, model_path)

    # Save summary
    summary = {
        "model": args.model,
        "target_column": args.target,
        "features": features,
        "mae": mae,
        "r2": r2,
        "contractor_recommendations": recommend_contractors(df),
    }

    summary_path = f"ml_models/models/{args.model}_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"📦 Model saved to {model_path}")
    print(f"📈 Summary saved to {summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train ML model on property maintenance data"
    )
    parser.add_argument("--model", required=True, help="Name of model")
    parser.add_argument(
        "--target", required=True, help="Target column (e.g. monthly_cost)"
    )
    parser.add_argument(
        "--features", required=True, help="Comma-separated list of features"
    )
    parser.add_argument("--data", required=True, help="Path to CSV data file")

    args = parser.parse_args()
    train_model(args)
