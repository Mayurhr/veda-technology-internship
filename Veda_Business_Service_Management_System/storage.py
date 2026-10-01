import json
import os


DATA_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data"
)


def _filepath(filename):
    """Return the full path of a data file."""

    return os.path.join(DATA_FOLDER, filename)


def load_data(filename, default=None):
    """
    Load records from a JSON file.

    - Missing file: creates it (with `default` records if given) and returns them.
    - Invalid/corrupted JSON: the bad file is backed up as <name>.corrupt
      (so it is never silently overwritten) and an empty list is returned.
    - Only dictionary records are returned.
    """

    os.makedirs(DATA_FOLDER, exist_ok=True)

    filepath = _filepath(filename)

    try:
        if not os.path.exists(filepath):
            records = [dict(item) for item in (default or [])]
            save_data(filename, records)
            return records

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]

        print(f"Warning: {filename} does not contain a list of records.")
        return []

    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON data in {filename}.")

        try:
            os.replace(filepath, filepath + ".corrupt")
            print(f"The damaged file was kept as {filename}.corrupt")
        except OSError:
            pass

        return []

    except OSError as error:
        print(f"File error while reading {filename}: {error}")
        return []


def save_data(filename, data):
    """
    Save records to a JSON file.

    Writes to a temporary file first so a failed save
    cannot damage the existing data. Returns True/False.
    """

    os.makedirs(DATA_FOLDER, exist_ok=True)

    filepath = _filepath(filename)
    temp_path = filepath + ".tmp"

    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        os.replace(temp_path, filepath)
        return True

    except OSError as error:
        print(f"File error while saving {filename}: {error}")
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
