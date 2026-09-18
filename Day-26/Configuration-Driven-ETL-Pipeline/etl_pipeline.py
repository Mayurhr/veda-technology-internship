import json
import logging
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).parent
CONFIG_FILE = PROJECT_DIR / "config.json"
LOG_FILE = PROJECT_DIR / "pipeline.log"


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )
    return logging.getLogger("etl_pipeline")


logger = setup_logging()


def load_config(config_file=CONFIG_FILE):
    with open(config_file, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_data(input_path):
    data = pd.read_csv(input_path)
    logger.info("Raw record count: %s", len(data))
    return data


def transform_data(data, settings):
    transformed = data.copy()

    if settings.get("strip_text", False):
        for column in settings.get("text_columns", []):
            transformed[column] = transformed[column].astype(str).str.strip()

    if settings.get("uppercase_category", False):
        category_column = settings.get("category_column", "category")
        transformed[category_column] = transformed[category_column].str.upper()

    status_filter = settings.get("status_filter")
    if status_filter:
        transformed = transformed[
            transformed[settings.get("status_column", "status")] == status_filter
        ].copy()

    if settings.get("add_total_value", False):
        quantity_column = settings.get("quantity_column", "quantity")
        price_column = settings.get("unit_price_column", "unit_price")
        total_column = settings.get("total_column", "total_value")
        transformed[total_column] = (
            transformed[quantity_column] * transformed[price_column]
        ).round(2)

    logger.info("Transformed record count: %s", len(transformed))
    return transformed


def validate_data(data, validation_rules):
    missing_columns = [
        column
        for column in validation_rules.get("required_columns", [])
        if column not in data.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    for column in validation_rules.get("no_null_columns", []):
        if data[column].isnull().any():
            raise ValueError(f"Null values found in required column: {column}")

    minimum_rows = validation_rules.get("minimum_rows", 0)
    if len(data) < minimum_rows:
        raise ValueError(
            f"Validation requires at least {minimum_rows} rows; found {len(data)}"
        )

    for column in validation_rules.get("non_negative_columns", []):
        if (data[column] < 0).any():
            raise ValueError(f"Negative value found in column: {column}")

    logger.info("Validation result: passed")
    return True


def save_data(data, output_path):
    data.to_csv(output_path, index=False)


def save_final_output(data, output_path):
    save_data(data, output_path)
    logger.info("Final record count: %s", len(data))


def load_final_output(output_path):
    return pd.read_csv(output_path)


def run_pipeline(config_file=CONFIG_FILE):
    logger.info("Pipeline started")
    config = load_config(config_file)
    paths = config["paths"]
    input_path = PROJECT_DIR / paths["input"]
    transformed_path = PROJECT_DIR / paths["transformed"]
    final_path = PROJECT_DIR / paths["final"]

    try:
        raw_data = extract_data(input_path)
        transformed_data = transform_data(raw_data, config["transformations"])
        save_data(transformed_data, transformed_path)
        validate_data(transformed_data, config["validation"])
        save_final_output(transformed_data, final_path)
        loaded_final_data = load_final_output(final_path)
        logger.info("Pipeline completed successfully")
        return loaded_final_data
    except (OSError, KeyError, ValueError, pd.errors.ParserError) as error:
        logger.error("Pipeline failed: %s", error)
        raise


if __name__ == "__main__":
    try:
        run_pipeline()
        print("ETL pipeline completed successfully.")
    except (OSError, KeyError, ValueError, pd.errors.ParserError) as error:
        print(f"ETL pipeline failed: {error}")