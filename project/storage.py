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

    If the file does not exist, it is created
    with the provided default data.

    If the file contains invalid JSON, the
    default data is restored.
    """

    file_path = os.path.join(
        DATA_FOLDER,
        filename
    )

    # Create data folder if it does not exist
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    # Create file with default data if it does not exist
    if not os.path.exists(file_path):
        save_data(filename, default_data)
        return default_data

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            # Make sure the JSON contains a list
            if not isinstance(data, list):
                print(
                    f"Warning: {filename} does not contain "
                    "valid list data."
                )
                save_data(filename, default_data)
                return default_data

            return data

    except json.JSONDecodeError:
        print(
            f"Warning: {filename} contains invalid JSON. "
            "Resetting to default data."
        )

        save_data(filename, default_data)
        return default_data

    except OSError as error:
        print(
            f"Error reading {filename}: {error}"
        )

        return default_data


def save_data(filename, data):
    """
    Save data to a JSON file inside the data folder.
    """

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    file_path = os.path.join(
        DATA_FOLDER,
        filename
    )

    try:
        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except OSError as error:
        print(
            f"Error saving {filename}: {error}"
        )


def generate_next_id(records, id_field, prefix):
    """
    Generate the next unique ID for a list of record dictionaries.

    Examples:
        PRG001, PRG002, PRG003
        SVC001, SVC002, SVC003
        INQ001, INQ002, INQ003
    """

    if not records:
        return f"{prefix}001"

    max_number = 0

    for record in records:

        existing_id = str(
            record.get(id_field, "")
        )

        if existing_id.startswith(prefix):

            number_part = existing_id[
                len(prefix):
            ]

            if number_part.isdigit():

                max_number = max(
                    max_number,
                    int(number_part)
                )

    return f"{prefix}{max_number + 1:03d}"