import argparse
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).parent
DEFAULT_INPUT_FILE = PROJECT_DIR / "sample_data.csv"
DEFAULT_REPORT_FILE = PROJECT_DIR / "quality_report.txt"
DEFAULT_INVALID_FILE = PROJECT_DIR / "invalid_records.csv"


def load_csv(input_file):
    """Load a CSV file and return it as a DataFrame."""
    try:
        return pd.read_csv(input_file)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Input file not found: {input_file}") from error
    except pd.errors.ParserError as error:
        raise ValueError(f"Could not read CSV file: {input_file}") from error


def check_missing_values(data):
    """Return missing-value counts for every column."""
    return data.isnull().sum()


def check_duplicates(data):
    """Return a mask for duplicate records and the duplicate count."""
    duplicate_mask = data.duplicated(keep=False)
    return duplicate_mask, int(data.duplicated().sum())


def check_data_types(data):
    """Report inferred types and columns with mixed numeric/text values."""
    data_types = data.dtypes.astype(str)
    unexpected_types = {}

    for column in data.columns:
        values = data[column].dropna()
        if values.empty or not pd.api.types.is_string_dtype(data[column]):
            continue

        numeric_values = pd.to_numeric(values, errors="coerce")
        numeric_count = int(numeric_values.notna().sum())
        if 0 < numeric_count < len(values):
            unexpected_types[column] = (
                f"mixed values ({numeric_count} numeric, "
                f"{len(values) - numeric_count} non-numeric)"
            )

    return data_types, unexpected_types


def calculate_unique_counts(data):
    """Return the number of distinct non-missing values in each column."""
    return data.nunique(dropna=True)


def calculate_completeness(data):
    """Return the percentage of non-missing values in each column."""
    if len(data) == 0:
        return pd.Series(0.0, index=data.columns)
    return (data.notna().sum() / len(data) * 100).round(2)


def calculate_uniqueness(data):
    """Return the percentage of unique non-missing values in each column."""
    if len(data) == 0:
        return pd.Series(0.0, index=data.columns)
    return (data.nunique(dropna=True) / len(data) * 100).round(2)


def identify_suspicious_records(data):
    """Return records containing common, easy-to-understand quality issues."""
    suspicious_mask = data.isnull().any(axis=1)
    duplicate_mask, _ = check_duplicates(data)
    suspicious_mask = suspicious_mask | duplicate_mask

    for column in data.select_dtypes(include=np.number).columns:
        suspicious_mask = suspicious_mask | (data[column] < 0).fillna(False)

    invalid_markers = {"unknown", "invalid", "n/a", "na", "null"}
    for column in data.select_dtypes(include=["object", "str"]).columns:
        marker_mask = data[column].astype("string").str.strip().str.lower().isin(
            invalid_markers
        )
        suspicious_mask = suspicious_mask | marker_mask.fillna(False)

    _, unexpected_types = check_data_types(data)
    for column in unexpected_types:
        values = pd.to_numeric(data[column], errors="coerce")
        suspicious_mask = suspicious_mask | (values.isna() & data[column].notna())

    suspicious_records = data.loc[suspicious_mask].copy()
    if not suspicious_records.empty:
        suspicious_records.insert(0, "source_row", suspicious_records.index + 2)
    return suspicious_records


def format_column_values(values):
    """Format a Series as readable report lines."""
    return "\n".join(f"  - {column}: {value}" for column, value in values.items())


def generate_quality_report(data, report_file, invalid_file):
    """Create the text quality report and invalid-record CSV."""
    missing_values = check_missing_values(data)
    _, duplicate_count = check_duplicates(data)
    data_types, unexpected_types = check_data_types(data)
    unique_counts = calculate_unique_counts(data)
    completeness = calculate_completeness(data)
    uniqueness = calculate_uniqueness(data)
    suspicious_records = identify_suspicious_records(data)

    report_lines = [
        "DATA QUALITY REPORT",
        "===================",
        f"Total records: {len(data)}",
        f"Total columns: {len(data.columns)}",
        "",
        "Missing values by column:",
        format_column_values(missing_values),
        "",
        f"Duplicate record count: {duplicate_count}",
        "",
        "Data types:",
        format_column_values(data_types),
        "",
        "Unexpected or mixed data types:",
        format_column_values(pd.Series(unexpected_types))
        if unexpected_types
        else "  - None detected",
        "",
        "Unique-value counts:",
        format_column_values(unique_counts),
        "",
        "Completeness metrics (% non-missing):",
        format_column_values(completeness),
        "",
        "Uniqueness metrics (% unique non-missing):",
        format_column_values(uniqueness),
        "",
        f"Suspicious or invalid records: {len(suspicious_records)}",
        "Invalid records saved to: " + str(invalid_file),
    ]

    Path(report_file).write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    suspicious_records.to_csv(invalid_file, index=False)
    return "\n".join(report_lines)


def run_quality_report(input_file=DEFAULT_INPUT_FILE, report_file=DEFAULT_REPORT_FILE,
                       invalid_file=DEFAULT_INVALID_FILE):
    """Load a CSV, profile it, and write both report files."""
    try:
        data = load_csv(input_file)
        report = generate_quality_report(data, report_file, invalid_file)
        return data, report
    except (OSError, ValueError, TypeError) as error:
        raise RuntimeError(f"Quality report failed: {error}") from error


def parse_arguments():
    parser = argparse.ArgumentParser(description="Profile a CSV data set.")
    parser.add_argument("input_file", nargs="?", type=Path, default=DEFAULT_INPUT_FILE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT_FILE)
    parser.add_argument("--invalid", type=Path, default=DEFAULT_INVALID_FILE)
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    try:
        data, _ = run_quality_report(
            arguments.input_file, arguments.report, arguments.invalid
        )
        print("Data-quality report generated successfully.")
        print(f"Records analyzed: {len(data)}")
        print(f"Columns analyzed: {len(data.columns)}")
        print(f"Quality report: {arguments.report.name}")
        print(f"Invalid records: {arguments.invalid.name}")
    except RuntimeError as error:
        print(error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())