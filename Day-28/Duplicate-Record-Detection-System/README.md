# Duplicate Record Detection System

## Description

This beginner-friendly Python program identifies exact and near-duplicate customer records. It uses Pandas for CSV processing and Python's `difflib` for simple fuzzy matching.

## Objective

The objective is to practice record matching, data cleaning, normalization, and safe duplicate handling in a small data-processing workflow.

## Tools Used

- Python
- Pandas
- `difflib`
- CSV files

## Features

- Loads customer records from a CSV file.
- Normalizes names, email addresses, phone numbers, and cities.
- Finds exact duplicate records.
- Finds potential near-duplicate pairs.
- Removes repeated exact records from the cleaned dataset.
- Regenerates all output files safely on every run.
- Handles missing files and invalid CSV input with clear errors.

## Project Structure

```text
Duplicate-Record-Detection-System/
├── duplicate_detector.py
├── sample_data.csv
├── exact_duplicates.csv
├── potential_duplicates.csv
├── cleaned_data.csv
├── sample_output.txt
└── README.md
```

## How the System Works

The program loads the input CSV, creates normalized comparison values, checks complete duplicate groups, compares remaining records pair by pair, and writes three CSV outputs plus a text summary.

## Data Normalization

Text values are stripped, converted to lowercase, and reduced to single spaces. Phone numbers keep digits only, so spaces and hyphens do not affect comparison. The original input is retained in the exact-duplicate report, while the cleaned dataset contains normalized values.

## Exact Duplicate Detection

`detect_exact_duplicates()` uses normalized Pandas rows and returns every row belonging to an exact duplicate group. This includes both the original record and repeated copies.

## Near-Duplicate Detection

`detect_near_duplicates()` compares pairs with `difflib.SequenceMatcher`. A pair is reported when it shares a normalized email or phone number, or when its names are sufficiently similar and its city matches. Exact duplicate pairs are not repeated in this report.

## Matching Fields

The important matching fields are `customer_name`, `email`, `phone`, and `city`. The customer ID and spending amount are kept as record data but are not used as the primary identity check.

## Cleaning Process

The cleaned dataset uses normalized values and keeps the first row from each exact duplicate group. Potential duplicates remain available in `potential_duplicates.csv` for a human review instead of being deleted automatically.

## Installation

Install the required dependency with:

```text
python -m pip install -r requirements.txt
```

## How to Run

From this project folder, run:

```text
python duplicate_detector.py
```

An alternate input CSV can be provided as the first argument:

```text
python duplicate_detector.py path/to/customer_data.csv
```

## Output Files

- `exact_duplicates.csv` contains all records in normalized exact-duplicate groups.
- `potential_duplicates.csv` contains near-duplicate pairs and similarity scores.
- `cleaned_data.csv` contains normalized records after exact duplicates are removed.
- `sample_output.txt` contains a readable summary of the sample run.

## Sample Output

```text
DUPLICATE RECORD DETECTION REPORT
=================================
Total records: 10
Exact duplicate records found: 3
Potential duplicate pairs found: 2
Cleaned record count: 8
Duplicate detection completed successfully.
```

## Concepts Learned

- CSV processing with Pandas
- Text and phone-number normalization
- Exact duplicate detection
- Fuzzy string matching with `difflib`
- Duplicate review workflows
- Safe file handling and repeatable output generation

## Conclusion

This project demonstrates a practical first step toward improving customer data quality. Exact duplicates can be cleaned automatically, while near duplicates are reported for careful review.