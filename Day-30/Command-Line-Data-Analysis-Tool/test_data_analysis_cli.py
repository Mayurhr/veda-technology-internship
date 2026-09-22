"""
Unit tests for the Command-Line Data Analysis Tool.

Run with:
    python -m unittest Day-30/Command-Line-Data-Analysis-Tool/test_data_analysis_cli.py

Uses only Python's built-in unittest module (no pytest dependency).
"""

import os
import tempfile
import unittest

from data_analysis_cli import DataAnalyzer


SAMPLE_CSV_CONTENT = (
    "customer,product,category,quantity,price,region,sales\n"
    "Ravi Kumar,Wireless Mouse,Electronics,3,15.50,North,46.50\n"
    "Anita Sharma,Office Chair,Furniture,1,89.99,South,89.99\n"
    "John Mathews,Notebook Set,Stationery,10,2.25,East,22.50\n"
    "Priya Nair,Wireless Mouse,Electronics,2,15.50,West,31.00\n"
)


class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a small temporary CSV file for each test.
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, newline=""
        )
        self.temp_file.write(SAMPLE_CSV_CONTENT)
        self.temp_file.close()
        self.analyzer = DataAnalyzer(self.temp_file.name)

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_load_data_success(self):
        df = self.analyzer.load_data()
        self.assertEqual(len(df), 4)
        self.assertIn("sales", df.columns)

    def test_load_data_missing_file(self):
        bad_analyzer = DataAnalyzer("this_file_does_not_exist.csv")
        with self.assertRaises(FileNotFoundError):
            bad_analyzer.load_data()

    def test_validate_columns_success(self):
        self.analyzer.load_data()
        # Should not raise for valid columns.
        self.analyzer.validate_columns(["region", "sales"])

    def test_validate_columns_missing(self):
        self.analyzer.load_data()
        with self.assertRaises(ValueError):
            self.analyzer.validate_columns(["not_a_real_column"])

    def test_validate_numeric_column(self):
        self.analyzer.load_data()
        # 'sales' is numeric, should not raise.
        self.analyzer.validate_numeric_column("sales")
        # 'region' is text, should raise.
        with self.assertRaises(ValueError):
            self.analyzer.validate_numeric_column("region")

    def test_filter_data_match(self):
        self.analyzer.load_data()
        mask = self.analyzer.df["region"].astype(str).str.lower() == "north"
        result = self.analyzer.df[mask]
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["customer"], "Ravi Kumar")

    def test_group_data(self):
        self.analyzer.load_data()
        grouped = self.analyzer.df.groupby("category").size()
        self.assertEqual(grouped["Electronics"], 2)
        self.assertEqual(grouped["Furniture"], 1)
        self.assertEqual(grouped["Stationery"], 1)

    def test_statistics_calculation(self):
        self.analyzer.load_data()
        total_sales = self.analyzer.df["sales"].sum()
        self.assertAlmostEqual(total_sales, 189.99, places=2)


if __name__ == "__main__":
    unittest.main()
