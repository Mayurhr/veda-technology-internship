# Command-Line Data Analysis Tool

## 1. Description
A command-line tool that loads a CSV file and lets you generate summaries,
filter rows, group data, and calculate statistics — all through simple
command-line options powered by Pandas and argparse.

## 2. Objective
Combine Pandas, argparse, input validation, and reusable application design
into a single beginner-friendly CLI project (Day 30 of the Veda Technology
Python Programming Internship).

## 3. Technologies Used
- Python 3
- Pandas
- argparse (standard library)
- unittest (standard library)

## 4. Features
- Load any CSV file (path provided by the user, never hardcoded)
- `--summary` — dataset overview (rows, columns, types, preview)
- `--filter` — filter rows by column/value
- `--group` — group rows by a column with counts and sales totals
- `--stats` — descriptive statistics for a numeric column
- Friendly `--help` documentation
- Clear, non-crashing error messages for common mistakes

## 5. Project Structure
```
Command-Line-Data-Analysis-Tool/
├── data_analysis_cli.py       # Main CLI application
├── sample_data.csv            # Sample small-business dataset
├── sample_output.txt          # Real captured runs of the tool
├── test_data_analysis_cli.py  # unittest test suite
└── README.md
```

## 6. Dataset Description
`sample_data.csv` is a small, realistic small-business sales dataset with
these columns:

| Column   | Description                        |
|----------|-------------------------------------|
| customer | Customer name                       |
| product  | Product purchased                   |
| category | Product category                    |
| quantity | Units purchased                     |
| price    | Unit price                          |
| region   | Sales region (North/South/East/West)|
| sales    | Total sale amount                   |

## 7. Installation
```bash
pip install pandas
```
(`argparse` and `unittest` ship with Python, so nothing else is required.)

## 8. Command-Line Usage
```bash
python data_analysis_cli.py <csv_path> [options]
python data_analysis_cli.py --help
```

## 9. Available Commands
| Option           | Description                                      |
|-------------------|--------------------------------------------------|
| `--summary`        | Dataset overview                                 |
| `--filter COL VAL` | Filter rows where COL equals VAL                 |
| `--group COL`      | Group rows by COL                                |
| `--stats COL`      | Statistics for a numeric COL                     |

## 10. Summary Analysis
```bash
python data_analysis_cli.py sample_data.csv --summary
```
Shows row/column counts, column data types, and a preview of the first rows.

## 11. Filtering
```bash
python data_analysis_cli.py sample_data.csv --filter region North
```
Shows all rows where the given column matches the given value
(case-insensitive).

## 12. Grouping
```bash
python data_analysis_cli.py sample_data.csv --group category
```
Shows row counts per group, plus total sales per group when a `sales`
column is present.

## 13. Statistical Analysis
```bash
python data_analysis_cli.py sample_data.csv --stats sales
```
Shows count, mean, standard deviation, min, quartiles, max, and sum for a
numeric column.

## 14. Input Validation
- Confirms the CSV file exists before reading it
- Confirms the CSV can actually be parsed (not empty/corrupted)
- Confirms requested columns exist in the dataset
- Confirms a column is numeric before running `--stats` on it

## 15. Error Handling
Invalid input (missing file, missing column, non-numeric stats column,
etc.) produces a clear one-line error message and exits with status code
`1` — no raw Python tracebacks for normal user mistakes.

## 16. Testing
Run the test suite with Python's built-in `unittest`:
```bash
python -m unittest test_data_analysis_cli.py
```
The tests cover: CSV loading (success and missing file), column
validation, numeric-column validation, filtering, grouping, and
statistics calculations. All 8 tests pass.

## 17. Sample Output
See `sample_output.txt` for real captured runs of `--help`, `--summary`,
`--filter`, `--group`, `--stats`, and two error cases (missing file,
non-numeric stats column).

## 18. Concepts Learned
- Structuring a CLI app around a reusable class (`DataAnalyzer`)
- Using `argparse` for multi-option command-line interfaces
- Data loading, filtering, grouping, and aggregation with Pandas
- Defensive input validation and user-friendly error handling
- Writing unit tests with `unittest`

## 19. Future Improvements
- Expose the same analysis logic through a REST API
- Expand automated test coverage (edge cases, larger datasets)
- Further object-oriented refactoring (e.g. separate report classes)
- Add basic chart/visualization export (matplotlib)
- Optional database (SQLite) integration for larger datasets

*(These are ideas for future work — not implemented in this version.)*

## 20. Conclusion
This project brings together Pandas, argparse, and clean reusable design
into a small, practical CLI tool for exploring CSV data, addressing the
feedback areas of code organization, validation, and presentation quality
from earlier internship tasks.
