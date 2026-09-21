# PDF Report Generator

## Description

A Python program that reads business sales data from a CSV file, calculates summary metrics with Pandas, and automatically creates a professional PDF report with ReportLab.

## Objective

Learn automated document generation using Python by turning raw business data into a formatted PDF report containing summary information and tables.

## Tools Used

- Python 3
- Pandas (data loading and processing)
- ReportLab (PDF generation)

## Features

- Loads business data from a CSV file
- Validates required columns and removes incomplete or duplicate records
- Calculates summary metrics automatically
- Generates a PDF with a title, report date, summary, metrics, tables, and conclusion
- Reusable for any CSV file with the same column structure
- Handles missing, empty, or invalid files with clear error messages
- Safe to run repeatedly: the same files are overwritten, never duplicated

## Project Structure

```
Day-29/
└── PDF-Report-Generator/
    ├── pdf_report_generator.py
    ├── sample_data.csv
    ├── generated_report.pdf
    ├── sample_output.txt
    └── README.md
```

## Dataset Explanation

`sample_data.csv` contains 24 sales orders from January to March 2026.

| Column | Description |
|--------|-------------|
| Order ID | Unique order identifier |
| Date | Order date (YYYY-MM-DD) |
| Product | Product name |
| Category | Product category |
| Region | Sales region |
| Units | Number of units sold |
| Unit Price | Price per unit |

## Data Processing

1. Load the CSV file with `pd.read_csv()`
2. Check that all required columns exist
3. Drop rows with missing values
4. Drop duplicate rows using `Order ID`
5. Convert the `Date` column to real dates
6. Add a `Revenue` column (`Units` x `Unit Price`)
7. Sort the records by date

## Summary Metrics

- Report period (first and last order date)
- Total orders
- Total units sold
- Total revenue
- Average order value
- Top product by revenue
- Top region by revenue
- Revenue by category

## PDF Generation

The report is built with ReportLab's Platypus layout tools. Paragraphs, spacers, and tables are added to a list and passed to `SimpleDocTemplate`, which handles page layout automatically. Table headers repeat when the data table continues onto a second page, and each page has a page number.

All text and numbers come from the processed data, so nothing in the report is hardcoded.

## Report Structure

1. Report title
2. Report date
3. Summary
4. Summary metrics table
5. Revenue by category table
6. Business data table
7. Conclusion

## Installation

```
pip install -r requirements.txt
```

Or install the packages directly:

```
pip install pandas reportlab
```

## How to Run

From the repository root:

```
python Day-29/PDF-Report-Generator/pdf_report_generator.py
```

To generate a report from another CSV file with the same columns:

```
python Day-29/PDF-Report-Generator/pdf_report_generator.py path/to/your_data.csv
```

The output files `generated_report.pdf` and `sample_output.txt` are overwritten on every run.

## Sample Output

```
Loading data from sample_data.csv...
Loaded 24 records.
Calculating summary metrics...
Generating PDF report...
PDF report saved: generated_report.pdf
Summary saved: sample_output.txt

Report Period: 05 Jan 2026 to 31 Mar 2026
Total Orders: 24
Total Units Sold: 335
Total Revenue: $37,303.93
Average Order Value: $1,554.33
Top Product: Laptop ($17,980.00)
Top Region: North ($13,271.90)
Revenue by Category:
  Computers: $17,980.00
  Accessories: $9,102.39
  Furniture: $5,172.54
  Displays: $5,049.00

Report generation completed successfully.
```

## Concepts Learned

- Loading and cleaning CSV data with Pandas
- Adding calculated columns and using `groupby`
- Building PDFs with ReportLab Platypus (paragraphs, spacers, tables)
- Styling tables with `TableStyle`
- Writing reusable functions instead of hardcoding report content
- Handling file errors with `try/except`
- Making a script safe to run multiple times

## Conclusion

This project shows how Python can automate report creation from start to finish. Pandas prepares the data and calculates the metrics, and ReportLab turns the results into a clean PDF, so a new report can be created from any similar CSV file with a single command.
