"""
Command-Line Data Analysis Tool
--------------------------------
A beginner-friendly CLI tool that loads a CSV file and lets the user
generate summaries, filter rows, group data, and view statistics
using Pandas and argparse.

Usage examples:
    python data_analysis_cli.py sample_data.csv --summary
    python data_analysis_cli.py sample_data.csv --filter region North
    python data_analysis_cli.py sample_data.csv --group category
    python data_analysis_cli.py sample_data.csv --stats sales

Run "python data_analysis_cli.py --help" for full usage details.
"""

import argparse
import os
import sys

import pandas as pd


class DataAnalyzer:
    """
    Small helper class that wraps the loading, validation, and
    analysis logic for a single CSV dataset.

    Keeping this logic in one class (instead of loose functions)
    makes the tool easier to extend later (e.g. adding new report
    types or reusing it inside a future REST API).
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------
    def load_data(self):
        """Load the CSV file into a Pandas DataFrame with validation."""
        if not os.path.isfile(self.csv_path):
            raise FileNotFoundError(
                f"File not found: '{self.csv_path}'. "
                "Please check the path and try again."
            )

        try:
            self.df = pd.read_csv(self.csv_path)
        except pd.errors.EmptyDataError:
            raise ValueError(f"The file '{self.csv_path}' is empty.")
        except pd.errors.ParserError:
            raise ValueError(
                f"The file '{self.csv_path}' could not be parsed. "
                "Please make sure it is a valid CSV file."
            )

        if self.df.empty:
            raise ValueError(f"The file '{self.csv_path}' has no data rows.")

        return self.df

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate_columns(self, columns):
        """
        Check that every column name in `columns` exists in the
        loaded dataset. Raises a clear ValueError if not.
        """
        missing = [col for col in columns if col not in self.df.columns]
        if missing:
            available = ", ".join(self.df.columns)
            raise ValueError(
                f"Column(s) not found: {', '.join(missing)}. "
                f"Available columns are: {available}"
            )

    def validate_numeric_column(self, column):
        """Check that a column exists AND is numeric (for --stats)."""
        self.validate_columns([column])
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise ValueError(
                f"Column '{column}' is not numeric, so statistics cannot "
                "be calculated on it."
            )

    # ------------------------------------------------------------------
    # Analysis operations
    # ------------------------------------------------------------------
    def show_summary(self):
        """Print an overview of the dataset: shape, columns, dtypes, preview."""
        print("Dataset loaded successfully.")
        print(f"Rows: {len(self.df)}")
        print(f"Columns: {len(self.df.columns)}")
        print("\nColumn names and types:")
        for col, dtype in self.df.dtypes.items():
            print(f"  - {col} ({dtype})")

        print("\nPreview (first 5 rows):")
        print(self.df.head().to_string(index=False))
        print("\nAnalysis completed successfully.")

    def filter_data(self, column, value):
        """Filter rows where `column` equals `value` and print the result."""
        self.validate_columns([column])

        # Compare as strings so numeric and text columns both work
        # from the command line without extra type-casting logic.
        mask = self.df[column].astype(str).str.lower() == str(value).lower()
        result = self.df[mask]

        if result.empty:
            print(f"No rows found where '{column}' == '{value}'.")
            return

        print(f"Filtered results where '{column}' == '{value}':")
        print(result.to_string(index=False))
        print(f"\n{len(result)} matching row(s) found.")
        print("Analysis completed successfully.")

    def group_data(self, column):
        """Group rows by `column` and print row counts (and sales sum if present)."""
        self.validate_columns([column])

        print(f"Grouped results by '{column}':")
        counts = self.df.groupby(column).size().rename("row_count")

        if "sales" in self.df.columns and pd.api.types.is_numeric_dtype(self.df["sales"]):
            totals = self.df.groupby(column)["sales"].sum().rename("total_sales")
            grouped = pd.concat([counts, totals], axis=1)
        else:
            grouped = counts.to_frame()

        print(grouped.to_string())
        print("\nAnalysis completed successfully.")

    def show_statistics(self, column):
        """Print descriptive statistics (count, mean, min, max, etc.) for a numeric column."""
        self.validate_numeric_column(column)

        stats = self.df[column].describe()
        print(f"Statistics for column '{column}':")
        print(f"  Count : {stats['count']:.0f}")
        print(f"  Mean  : {stats['mean']:.2f}")
        print(f"  Std   : {stats['std']:.2f}")
        print(f"  Min   : {stats['min']:.2f}")
        print(f"  25%   : {stats['25%']:.2f}")
        print(f"  50%   : {stats['50%']:.2f}")
        print(f"  75%   : {stats['75%']:.2f}")
        print(f"  Max   : {stats['max']:.2f}")
        print(f"  Sum   : {self.df[column].sum():.2f}")
        print("\nAnalysis completed successfully.")


# ----------------------------------------------------------------------
# Argument parsing
# ----------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        prog="data_analysis_cli.py",
        description="A simple command-line tool to analyze CSV data using Pandas.",
        epilog=(
            "Examples:\n"
            "  python data_analysis_cli.py sample_data.csv --summary\n"
            "  python data_analysis_cli.py sample_data.csv --filter region North\n"
            "  python data_analysis_cli.py sample_data.csv --group category\n"
            "  python data_analysis_cli.py sample_data.csv --stats sales\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "csv_path",
        help="Path to the CSV file to analyze (required, not hardcoded).",
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show an overview of the dataset (rows, columns, preview).",
    )
    parser.add_argument(
        "--filter",
        nargs=2,
        metavar=("COLUMN", "VALUE"),
        help="Filter rows where COLUMN equals VALUE, e.g. --filter region North",
    )
    parser.add_argument(
        "--group",
        metavar="COLUMN",
        help="Group rows by COLUMN and show counts/totals, e.g. --group category",
    )
    parser.add_argument(
        "--stats",
        metavar="COLUMN",
        help="Show statistics (mean, min, max, etc.) for a numeric COLUMN, e.g. --stats sales",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not (args.summary or args.filter or args.group or args.stats):
        parser.error(
            "No analysis command given. Choose one of: "
            "--summary, --filter, --group, --stats (see --help for examples)."
        )

    analyzer = DataAnalyzer(args.csv_path)

    try:
        analyzer.load_data()

        if args.summary:
            analyzer.show_summary()
        if args.filter:
            column, value = args.filter
            analyzer.filter_data(column, value)
        if args.group:
            analyzer.group_data(args.group)
        if args.stats:
            analyzer.show_statistics(args.stats)

    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
