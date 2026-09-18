# Configuration-Driven ETL Pipeline

## Description

This project is a small ETL pipeline that reads sales records from a CSV file, applies transformations defined in JSON, validates the result, and writes the transformed and final datasets.

## Objective

The objective is to practice a simple, repeatable data-engineering workflow while keeping pipeline settings separate from Python code.

## Tools Used

- Python
- Pandas
- JSON configuration
- CSV data
- Python `logging` module

## ETL Workflow

1. Extract records from `data/raw.csv`.
2. Transform text, filter completed orders, and calculate total values using `config.json`.
3. Validate the transformed records using configured rules.
4. Load the valid records into `data/final.csv`.
5. Log counts and pipeline status in `pipeline.log`.

## Project Structure

```text
Configuration-Driven-ETL-Pipeline/
├── etl_pipeline.py
├── config.json
├── data/
│   ├── raw.csv
│   ├── transformed.csv
│   └── final.csv
├── pipeline.log
├── README.md
└── sample_output.txt
```

## Configuration Explanation

`config.json` contains the input and output paths, transformation settings, and validation rules. For example, `status_filter` controls which orders are loaded, while `add_total_value` controls whether `quantity * unit_price` is added as a new column.

## Extract Stage

`extract_data()` uses Pandas to read the configured input CSV and logs the number of raw records.

## Transform Stage

`transform_data()` copies the input data, trims configured text columns, converts categories to uppercase, keeps the configured status, and calculates the configured total column.

## Validation Stage

`validate_data()` checks required columns, null values, minimum record count, and non-negative numeric values from the configuration.

## Load Stage

`save_data()` writes the transformed dataset. `save_final_output()` writes the validated final dataset, and `load_final_output()` reads it back to confirm the output is usable.

## Logging

The pipeline writes timestamps, log levels, record counts, validation results, completion messages, and errors to `pipeline.log`.

## Error Handling

The pipeline uses `try/except` to log file, configuration, CSV, and validation errors before reporting a clear failure message. It writes fresh CSV output on every successful run, so repeated runs do not append duplicate records.

## Installation

```text
python -m pip install pandas
```

## How to Run

Open a terminal in this project folder and run:

```text
python etl_pipeline.py
```

## Sample Output

See `sample_output.txt` for an example successful execution.

## Concepts Learned

- Extract, transform, and load stages
- Pandas CSV processing
- Configuration-driven programming
- Data validation
- Repeatable file output
- Record-count logging
- Exception handling

## Conclusion

This project demonstrates how a small Python ETL workflow can be controlled by configuration, tested one stage at a time, validated before loading, and monitored through logs.