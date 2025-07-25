#!/usr/bin/env python3
"""
Data Sanitizer Component
========================

Handles data cleaning, PII redaction, and sanitization.
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class DataSanitizer:
    """
    Data sanitizer component for cleaning and redacting sensitive data.
    """

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Initialize the data sanitizer.

        Args:
            config: Configuration dictionary for sanitization rules
        """
        self.config = config or self._get_default_config()
        self.redaction_patterns = self._load_redaction_patterns()

        logger.info("🧹 Data sanitizer initialized")
        logger.info(f"   Redaction patterns: {len(self.redaction_patterns)} configured")

    def sanitize_data(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        Sanitize data from a file.

        Args:
            file_path: Path to the input file
            output_path: Path for the sanitized output (optional)

        Returns:
            Path to the sanitized file

        Raises:
            ValueError: If file format is not supported
        """
        input_path = Path(file_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        # Determine file type and sanitize accordingly
        if input_path.suffix.lower() == ".csv":
            return self._sanitize_csv(input_path, output_path)
        elif input_path.suffix.lower() in [".xlsx", ".xls"]:
            return self._sanitize_excel(input_path, output_path)
        elif input_path.suffix.lower() == ".json":
            return self._sanitize_json(input_path, output_path)
        elif input_path.suffix.lower() == ".txt":
            return self._sanitize_text(input_path, output_path)
        else:
            raise ValueError(f"Unsupported file format: {input_path.suffix}")

    def _sanitize_csv(self, input_path: Path, output_path: Optional[str] = None) -> str:
        """Sanitize CSV data."""
        logger.info(f"📊 Sanitizing CSV: {input_path}")

        # Read CSV
        try:
            df = pd.read_csv(input_path)
        except Exception as e:
            raise ValueError(f"Failed to read CSV file: {e}")

        # Sanitize the dataframe
        sanitized_df = self._sanitize_dataframe(df)

        # Generate output path
        if output_path is None:
            output_path = str(input_path).replace("uploaded", "cleaned")

        # Save sanitized data
        sanitized_df.to_csv(output_path, index=False)

        logger.info(f"✅ CSV sanitized: {output_path}")
        return output_path

    def _sanitize_excel(
        self, input_path: Path, output_path: Optional[str] = None
    ) -> str:
        """Sanitize Excel data."""
        logger.info(f"📊 Sanitizing Excel: {input_path}")

        # Read Excel
        try:
            df = pd.read_excel(input_path)
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {e}")

        # Sanitize the dataframe
        sanitized_df = self._sanitize_dataframe(df)

        # Generate output path
        if output_path is None:
            output_path = str(input_path).replace("uploaded", "cleaned")

        # Save sanitized data
        sanitized_df.to_excel(output_path, index=False)

        logger.info(f"✅ Excel sanitized: {output_path}")
        return output_path

    def _sanitize_json(
        self, input_path: Path, output_path: Optional[str] = None
    ) -> str:
        """Sanitize JSON data."""
        logger.info(f"📊 Sanitizing JSON: {input_path}")

        # Read JSON
        try:
            with open(input_path) as f:
                data = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to read JSON file: {e}")

        # Sanitize the data
        sanitized_data = self._sanitize_json_data(data)

        # Generate output path
        if output_path is None:
            output_path = str(input_path).replace("uploaded", "cleaned")

        # Save sanitized data
        with open(output_path, "w") as f:
            json.dump(sanitized_data, f, indent=2)

        logger.info(f"✅ JSON sanitized: {output_path}")
        return output_path

    def _sanitize_text(
        self, input_path: Path, output_path: Optional[str] = None
    ) -> str:
        """Sanitize text data."""
        logger.info(f"📊 Sanitizing text: {input_path}")

        # Read text
        try:
            with open(input_path) as f:
                text = f.read()
        except Exception as e:
            raise ValueError(f"Failed to read text file: {e}")

        # Sanitize the text
        sanitized_text = self._sanitize_text_content(text)

        # Generate output path
        if output_path is None:
            output_path = str(input_path).replace("uploaded", "cleaned")

        # Save sanitized data
        with open(output_path, "w") as f:
            f.write(sanitized_text)

        logger.info(f"✅ Text sanitized: {output_path}")
        return output_path

    def _sanitize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sanitize a pandas DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            Sanitized DataFrame
        """
        logger.info(
            f"   Processing DataFrame: {df.shape[0]} rows, {df.shape[1]} columns"
        )

        # Create a copy to avoid modifying the original
        sanitized_df = df.copy()

        # Apply redaction patterns to each column
        for column in sanitized_df.columns:
            if sanitized_df[column].dtype == "object":
                sanitized_df[column] = sanitized_df[column].apply(
                    lambda x: self._redact_sensitive_data(str(x)) if pd.notna(x) else x
                )

        # Remove duplicate rows
        original_rows = len(sanitized_df)
        sanitized_df = sanitized_df.drop_duplicates()
        removed_rows = original_rows - len(sanitized_df)

        if removed_rows > 0:
            logger.info(f"   Removed {removed_rows} duplicate rows")

        # Handle missing values
        sanitized_df = self._handle_missing_values(sanitized_df)

        # Validate data types
        sanitized_df = self._validate_data_types(sanitized_df)

        logger.info(
            f"   Sanitization completed: {sanitized_df.shape[0]} rows, {sanitized_df.shape[1]} columns"
        )

        return sanitized_df

    def _sanitize_json_data(self, data: Any) -> Any:
        """
        Recursively sanitize JSON data.

        Args:
            data: Input data (dict, list, or primitive)

        Returns:
            Sanitized data
        """
        if isinstance(data, dict):
            return {key: self._sanitize_json_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_json_data(item) for item in data]
        elif isinstance(data, str):
            return self._redact_sensitive_data(data)
        else:
            return data

    def _sanitize_text_content(self, text: str) -> str:
        """
        Sanitize text content.

        Args:
            text: Input text

        Returns:
            Sanitized text
        """
        # Apply redaction patterns
        sanitized_text = self._redact_sensitive_data(text)

        # Remove excessive whitespace
        sanitized_text = re.sub(r"\s+", " ", sanitized_text)

        return sanitized_text.strip()

    def _redact_sensitive_data(self, text: str) -> str:
        """
        Redact sensitive data from text.

        Args:
            text: Input text

        Returns:
            Text with sensitive data redacted
        """
        if not isinstance(text, str):
            return text

        redacted_text = text

        # Apply redaction patterns
        for _pattern_name, pattern_info in self.redaction_patterns.items():
            pattern = pattern_info["pattern"]
            replacement = pattern_info["replacement"]

            if pattern_info.get("enabled", True):
                redacted_text = re.sub(
                    pattern, replacement, redacted_text, flags=re.IGNORECASE
                )

        return redacted_text

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with handled missing values
        """
        # Count missing values
        missing_counts = df.isnull().sum()
        if missing_counts.sum() > 0:
            logger.info(f"   Missing values found: {missing_counts.to_dict()}")

        # Handle missing values based on data type
        for column in df.columns:
            if df[column].isnull().sum() > 0:
                if df[column].dtype in ["int64", "float64"]:
                    # For numeric columns, fill with median
                    median_value = df[column].median()
                    df[column].fillna(median_value, inplace=True)
                else:
                    # For categorical/text columns, fill with mode or 'Unknown'
                    mode_value = df[column].mode()
                    fill_value = mode_value[0] if len(mode_value) > 0 else "Unknown"
                    df[column].fillna(fill_value, inplace=True)

        return df

    def _validate_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate and convert data types.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with validated data types
        """
        for column in df.columns:
            # Try to convert numeric columns
            if df[column].dtype == "object":
                # Check if column contains numeric data
                numeric_values = pd.to_numeric(df[column], errors="coerce")
                if not numeric_values.isna().all():
                    # If most values are numeric, convert the column
                    non_null_ratio = numeric_values.notna().sum() / len(df)
                    if non_null_ratio > 0.8:  # 80% of values are numeric
                        df[column] = numeric_values
                        logger.debug(f"   Converted column '{column}' to numeric")

        return df

    def _get_default_config(self) -> dict[str, Any]:
        """Get default configuration."""
        return {
            "remove_duplicates": True,
            "handle_missing_values": True,
            "validate_data_types": True,
            "redaction_enabled": True,
            "log_level": "INFO",
        }

    def _load_redaction_patterns(self) -> dict[str, dict[str, Any]]:
        """Load redaction patterns."""
        return {
            "email": {
                "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "replacement": "[EMAIL_REDACTED]",
                "enabled": True,
            },
            "phone": {
                "pattern": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
                "replacement": "[PHONE_REDACTED]",
                "enabled": True,
            },
            "ssn": {
                "pattern": r"\b\d{3}-\d{2}-\d{4}\b",
                "replacement": "[SSN_REDACTED]",
                "enabled": True,
            },
            "credit_card": {
                "pattern": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
                "replacement": "[CC_REDACTED]",
                "enabled": True,
            },
            "ip_address": {
                "pattern": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
                "replacement": "[IP_REDACTED]",
                "enabled": True,
            },
            "url": {
                "pattern": r'https?://[^\s<>"]+|www\.[^\s<>"]+\b',
                "replacement": "[URL_REDACTED]",
                "enabled": True,
            },
            "api_key": {
                "pattern": r"\b[A-Za-z0-9]{32,}\b",
                "replacement": "[API_KEY_REDACTED]",
                "enabled": True,
            },
        }

    def add_redaction_pattern(
        self, name: str, pattern: str, replacement: str, enabled: bool = True
    ):
        """
        Add a custom redaction pattern.

        Args:
            name: Pattern name
            pattern: Regex pattern
            replacement: Replacement string
            enabled: Whether the pattern is enabled
        """
        self.redaction_patterns[name] = {
            "pattern": pattern,
            "replacement": replacement,
            "enabled": enabled,
        }
        logger.info(f"🔧 Added redaction pattern: {name}")

    def get_sanitization_report(
        self, input_path: str, output_path: str
    ) -> dict[str, Any]:
        """
        Generate a sanitization report.

        Args:
            input_path: Path to input file
            output_path: Path to output file

        Returns:
            Sanitization report
        """
        input_path_obj = Path(input_path)
        output_path_obj = Path(output_path)

        report = {
            "input_file": str(input_path),
            "output_file": str(output_path),
            "input_size": (
                input_path_obj.stat().st_size if input_path_obj.exists() else 0
            ),
            "output_size": (
                output_path_obj.stat().st_size if output_path_obj.exists() else 0
            ),
            "file_type": input_path_obj.suffix.lower(),
            "sanitization_timestamp": datetime.now().isoformat(),
            "redaction_patterns_applied": list(self.redaction_patterns.keys()),
            "config": self.config,
        }

        return report


def sanitize_data(file_path: str) -> str:
    """
    Convenience function to sanitize data.

    Args:
        file_path: Path to the input file

    Returns:
        Path to the sanitized file
    """
    sanitizer = DataSanitizer()
    return sanitizer.sanitize_data(file_path)


if __name__ == "__main__":
    # Example usage
    print("🧹 Data Sanitizer Demo")
    print("=" * 30)

    # Create example data with sensitive information
    example_data = {
        "name": ["John Doe", "Jane Smith", "Bob Johnson"],
        "email": ["john@example.com", "jane@company.com", "bob@gmail.com"],
        "phone": ["555-123-4567", "555-987-6543", "555-555-5555"],
        "ssn": ["123-45-6789", "987-65-4321", "111-22-3333"],
        "value": [100, 200, 300],
    }

    df = pd.DataFrame(example_data)
    input_file = "/tmp/sensitive_data.csv"
    df.to_csv(input_file, index=False)

    print(f"📝 Created test data: {input_file}")

    # Test sanitization
    sanitizer = DataSanitizer()
    output_file = sanitizer.sanitize_data(input_file)

    print(f"✅ Data sanitized: {output_file}")

    # Show results
    sanitized_df = pd.read_csv(output_file)
    print("\n📊 Sanitization Results:")
    print(sanitized_df)

    # Generate report
    report = sanitizer.get_sanitization_report(input_file, output_file)
    print(f"\n📋 Report: {report['input_size']} bytes -> {report['output_size']} bytes")

    print("🎉 Data sanitizer demo completed!")
