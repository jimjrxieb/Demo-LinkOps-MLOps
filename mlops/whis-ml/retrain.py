#!/usr/bin/env python3
"""
Automated retraining script for the ML Task Classifier orb.
Updates the model based on new approved tasks from the system.
"""

import json
import os
from datetime import datetime

import pandas as pd
from train_classifier import train_model


def load_existing_data():
    """Load existing training data."""
    try:
        return pd.read_csv("dataset/tasks.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["task", "category"])


def load_new_tasks():
    """Load new approved tasks from the system."""
    try:
        with open("dataset/new_tasks.json") as f:
            new_tasks = json.load(f)
        return pd.DataFrame(new_tasks)
    except FileNotFoundError:
        return pd.DataFrame(columns=["task", "category"])


def merge_and_save_data(existing_df, new_df):
    """Merge existing and new data, save updated dataset."""
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=["task"])
    combined_df.to_csv("dataset/tasks.csv", index=False)
    return combined_df


def backup_model():
    """Create a backup of the current model."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)

    if os.path.exists("classifier_model.h5"):
        os.system(f"cp classifier_model.h5 {backup_dir}/")
    if os.path.exists("tokenizer.pkl"):
        os.system(f"cp tokenizer.pkl {backup_dir}/")
    if os.path.exists("label_encoder.pkl"):
        os.system(f"cp label_encoder.pkl {backup_dir}/")

    return backup_dir


def main():
    """Main retraining function."""
    print("🔄 Starting automated retraining...")

    # Load existing data
    existing_data = load_existing_data()
    print(f"📊 Loaded {len(existing_data)} existing training examples")

    # Load new tasks
    new_tasks = load_new_tasks()
    print(f"🆕 Found {len(new_tasks)} new tasks to add")

    if len(new_tasks) == 0:
        print("✅ No new tasks to add. Model is up to date.")
        return

    # Backup current model
    backup_dir = backup_model()
    print(f"💾 Backed up current model to {backup_dir}")

    # Merge and save data
    combined_data = merge_and_save_data(existing_data, new_tasks)
    print(f"📈 Combined dataset now has {len(combined_data)} examples")

    # Retrain model
    print("🧠 Retraining model...")
    train_model()

    # Clear new tasks file
    if os.path.exists("dataset/new_tasks.json"):
        os.remove("dataset/new_tasks.json")

    print("✅ Retraining complete! Model updated with new data.")


if __name__ == "__main__":
    main()
