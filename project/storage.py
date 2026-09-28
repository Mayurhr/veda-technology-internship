"""
storage.py

Simple helper functions to load and save JSON data files.
Used by programs.py, services.py, and inquiries.py.
"""

import json
import os

DATA_FOLDER = "data"


def load_data(filename, default_data):
    """
    Load data from a JSON file inside the data folder.
    If the file does not exist, create it with default_data first.
    """
    file_path = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    if not os.path.exists(file_path):
        save_data(filename, default_data)
        return default_data

    with open(file_path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            # If the file is empty or corrupted, reset it safely
            save_data(filename, default_data)
            return default_data


def save_data(filename, data):
    """
    Save data to a JSON file inside the data folder.
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    file_path = os.path.join(DATA_FOLDER, filename)
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def generate_next_id(records, id_field, prefix):
    """
    Generate the next unique ID for a list of record dictionaries.
    Example: PRG001, PRG002, ...
    """
    if not records:
        return f"{prefix}001"

    max_number = 0
    for record in records:
        existing_id = record[id_field]
        number_part = existing_id.replace(prefix, "")
        if number_part.isdigit():
            max_number = max(max_number, int(number_part))

    return f"{prefix}{max_number + 1:03d}"
