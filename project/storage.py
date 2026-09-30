import json
import csv
import os


DATA_FOLDER = "data"


def load_data(filename):
    """
    Load records from a JSON file.

    Returns an empty list if the file does not exist
    or contains invalid data.
    """

    os.makedirs(DATA_FOLDER, exist_ok=True)

    filepath = os.path.join(DATA_FOLDER, filename)

    try:
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

            return []

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON data in {filename}.")
        return []

    except OSError as error:
        print(f"File error while reading {filename}: {error}")
        return []


def save_data(filename, data):
    """
    Save records to a JSON file.
    """

    os.makedirs(DATA_FOLDER, exist_ok=True)

    filepath = os.path.join(DATA_FOLDER, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except OSError as error:
        print(f"File error while saving {filename}: {error}")
        return False


def load_csv_data(filename):
    """
    Load records from a CSV file.

    Returns a list of dictionaries.
    """

    os.makedirs(DATA_FOLDER, exist_ok=True)

    filepath = os.path.join(DATA_FOLDER, filename)

    try:
        if not os.path.exists(filepath):
            return []

        with open(
            filepath,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            return list(reader)

    except OSError as error:
        print(f"CSV file error while reading {filename}: {error}")
        return []


def save_csv_data(filename, data):
    """
    Save records to a CSV file.
    """

    os.makedirs(DATA_FOLDER, exist_ok=True)

    filepath = os.path.join(DATA_FOLDER, filename)

    try:
        if not data:
            with open(
                filepath,
                "w",
                newline="",
                encoding="utf-8"
            ):
                pass

            return True

        fieldnames = data[0].keys()

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(data)

        return True

    except OSError as error:
        print(f"CSV file error while saving {filename}: {error}")
        return False


def generate_next_id(records, prefix, field):
    """
    Generate the next sequential ID.

    Example:
    PRG001
    PRG002
    PRG003
    """

    numbers = []

    for record in records:

        record_id = str(record.get(field, ""))

        if record_id.startswith(prefix):

            try:
                number = int(
                    record_id[len(prefix):]
                )

                numbers.append(number)

            except ValueError:
                continue

    next_number = max(numbers, default=0) + 1

    return f"{prefix}{next_number:03d}"