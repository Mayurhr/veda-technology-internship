# Data Quality Reporting Tool

## Description

This beginner-friendly Python tool profiles a CSV file and creates a practical data-quality report. It helps identify incomplete, duplicated, incorrectly typed, and suspicious records before data is used for analysis.

## Objective

The objective is to practice data-quality assessment techniques used in analytics and data engineering.

## Tools Used

- Python
- Pandas
- NumPy
- CSV files

## Features

- Loads any CSV file from the command line.
- Reports missing values and duplicate records.
- Displays inferred data types and mixed numeric/text values.
- Counts unique values in every column.
- Calculates completeness and uniqueness percentages.
- Finds suspicious records with missing values, duplicate rows, invalid markers, or negative numeric values.
- Creates text and CSV reports on every run.

## Project Structure

```text
Data-Quality-Reporting-Tool/
├── data_quality_report.py
├── sample_data.csv
├── quality_report.txt
├── invalid_records.csv
├── sample_output.txt
└── README.md
```

## How the Tool Works

The script reads the input CSV into a Pandas DataFrame, runs several small profiling functions, identifies suspicious rows, and writes a readable summary report plus a CSV containing the affected records.

## Missing-Value Analysis

`check_missing_values()` counts empty cells in each column. Completeness uses the same information to show the percentage of populated cells.

## Duplicate Detection

`check_duplicates()` counts repeated records and marks all rows that belong to a duplicate group for the invalid-record report.

## Data-Type Checking

`check_data_types()` reports the type inferred by Pandas for every column. It also flags object columns that contain a mixture of numeric and non-numeric values, such as an age column containing `unknown`.

## Unique-Value Analysis

`calculate_unique_counts()` counts distinct non-missing values in each column. This can reveal identifier columns, repeated categories, and columns with very little variation.

## Completeness

Completeness is the percentage of non-missing values in a column:

```text
non-missing values / total records * 100
```

## Uniqueness

Uniqueness is the percentage of distinct non-missing values compared with the total number of records:

```text
unique values / total records * 100
```

## Suspicious-Record Detection

`identify_suspicious_records()` marks rows with missing cells, duplicate records, negative numeric values, common invalid markers such as `unknown` or `invalid`, and non-numeric values in mixed numeric/text columns.

## Generated Reports

- `quality_report.txt` contains the complete profile and quality metrics.
- `invalid_records.csv` contains records identified as suspicious or invalid.
- `sample_output.txt` shows a successful sample execution.

## Installation

Install the required packages with:

```text
python -m pip install pandas numpy
```

## How to Run

From this project folder, run the sample profile:

```text
python data_quality_report.py
```

To profile another CSV, provide its path. Optional flags choose different output files:

```text
python data_quality_report.py path/to/data.csv --report my_report.txt --invalid my_invalid_records.csv
```

## Sample Output

See `sample_output.txt` for a successful execution summary. The full metrics are in `quality_report.txt`.

## Concepts Learned

- Data profiling with Pandas
- Missing-value analysis
- Duplicate detection
- Data-type validation
- Unique-value counts
- Completeness and uniqueness metrics
- Suspicious-record identification
- Reusable command-line scripts
- Safe file handling and report generation

## Conclusion

This project demonstrates a repeatable first step in data engineering: measure the quality of incoming data before using it in a report, analysis, or pipeline.