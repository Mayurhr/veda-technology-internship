import argparse
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).parent
DEFAULT_INPUT_FILE = PROJECT_DIR / "sample_data.csv"
DEFAULT_EXACT_FILE = PROJECT_DIR / "exact_duplicates.csv"
DEFAULT_POTENTIAL_FILE = PROJECT_DIR / "potential_duplicates.csv"
DEFAULT_CLEANED_FILE = PROJECT_DIR / "cleaned_data.csv"
DEFAULT_OUTPUT_FILE = PROJECT_DIR / "sample_output.txt"
MATCHING_FIELDS = ["customer_name", "email", "phone", "city"]


def load_csv(input_file):
    """Load customer records from a CSV file."""
    try:
        return pd.read_csv(input_file, dtype=str).fillna("")
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Input file not found: {input_file}") from error
    except pd.errors.ParserError as error:
        raise ValueError(f"Could not read CSV file: {input_file}") from error


def normalize_value(value, field_name=""):
    """Normalize text and simple contact formatting for comparisons."""
    value = str(value).strip().lower()
    value = " ".join(value.split())
    if field_name == "phone":
        return "".join(character for character in value if character.isdigit())
    return value


def normalize_data(data):
    """Return a copy with comparable values normalized."""
    normalized = data.copy()
    for column in MATCHING_FIELDS:
        if column in normalized.columns:
            normalized[column] = normalized[column].map(
                lambda value: normalize_value(value, column)
            )
    return normalized


def detect_exact_duplicates(data):
    """Return every record in a normalized exact-duplicate group."""
    normalized = normalize_data(data)
    duplicate_mask = normalized.duplicated(keep=False)
    duplicates = data.loc[duplicate_mask].copy()
    duplicates.insert(0, "source_row", duplicates.index + 2)
    return duplicates


def _similarity(first_record, second_record):
    scores = []
    for field in MATCHING_FIELDS:
        first_value = first_record.get(field, "")
        second_value = second_record.get(field, "")
        if first_value and second_value:
            scores.append(SequenceMatcher(None, first_value, second_value).ratio())
    return sum(scores) / len(scores) if scores else 0.0


def detect_near_duplicates(data, similarity_threshold=0.80):
    """Return non-exact record pairs that share a strong matching signal."""
    normalized = normalize_data(data)
    exact_mask = normalized.duplicated(keep=False)
    potential_matches = []

    for first_index, second_index in combinations(normalized.index, 2):
        if exact_mask.loc[first_index] and exact_mask.loc[second_index]:
            if normalized.loc[first_index].equals(normalized.loc[second_index]):
                continue

        first_record = normalized.loc[first_index]
        second_record = normalized.loc[second_index]
        shared_contact = any(
            first_record[field]
            and first_record[field] == second_record[field]
            for field in ("email", "phone")
            if field in normalized.columns
        )
        name_similarity = SequenceMatcher(
            None,
            first_record.get("customer_name", ""),
            second_record.get("customer_name", ""),
        ).ratio()
        same_city = (
            first_record.get("city", "")
            and first_record.get("city", "") == second_record.get("city", "")
        )

        if shared_contact or (name_similarity >= similarity_threshold and same_city):
            potential_matches.append(
                {
                    "first_source_row": first_index + 2,
                    "second_source_row": second_index + 2,
                    "first_customer_name": data.loc[first_index, "customer_name"],
                    "second_customer_name": data.loc[second_index, "customer_name"],
                    "first_email": data.loc[first_index, "email"],
                    "second_email": data.loc[second_index, "email"],
                    "similarity_score": round(_similarity(first_record, second_record), 2),
                }
            )

    return pd.DataFrame(potential_matches)


def clean_dataset(data):
    """Normalize values and keep the first copy of each exact record."""
    cleaned = normalize_data(data)
    return cleaned.drop_duplicates(keep="first").reset_index(drop=True)


def save_output(data, output_file):
    """Save a DataFrame as a CSV, replacing any previous output."""
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_file, index=False)


def generate_duplicate_reports(
    data, exact_file=DEFAULT_EXACT_FILE, potential_file=DEFAULT_POTENTIAL_FILE
):
    """Generate exact and potential duplicate CSV reports."""
    exact_duplicates = detect_exact_duplicates(data)
    potential_duplicates = detect_near_duplicates(data)
    save_output(exact_duplicates, exact_file)
    save_output(potential_duplicates, potential_file)
    return exact_duplicates, potential_duplicates


def save_outputs(data, exact_file, potential_file, cleaned_file):
    """Generate reports and save the cleaned dataset."""
    exact_duplicates, potential_duplicates = generate_duplicate_reports(
        data, exact_file, potential_file
    )
    save_output(clean_dataset(data), cleaned_file)
    return exact_duplicates, potential_duplicates


def run_detection(
    input_file=DEFAULT_INPUT_FILE,
    exact_file=DEFAULT_EXACT_FILE,
    potential_file=DEFAULT_POTENTIAL_FILE,
    cleaned_file=DEFAULT_CLEANED_FILE,
    output_file=DEFAULT_OUTPUT_FILE,
):
    """Run duplicate detection and write a human-readable summary."""
    data = load_csv(input_file)
    exact_duplicates, potential_duplicates = save_outputs(
        data, exact_file, potential_file, cleaned_file
    )
    cleaned_count = len(clean_dataset(data))
    report = "\n".join(
        [
            "DUPLICATE RECORD DETECTION REPORT",
            "=================================",
            f"Total records: {len(data)}",
            f"Exact duplicate records found: {len(exact_duplicates)}",
            f"Potential duplicate pairs found: {len(potential_duplicates)}",
            f"Cleaned record count: {cleaned_count}",
            "Duplicate detection completed successfully.",
        ]
    )
    Path(output_file).write_text(report + "\n", encoding="utf-8")
    return report


def parse_arguments():
    parser = argparse.ArgumentParser(description="Detect duplicate customer records.")
    parser.add_argument("input_file", nargs="?", type=Path, default=DEFAULT_INPUT_FILE)
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    try:
        print(run_detection(arguments.input_file))
    except (OSError, ValueError, TypeError) as error:
        print(f"Duplicate detection failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())