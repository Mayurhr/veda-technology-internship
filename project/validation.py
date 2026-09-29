"""
validation.py

Simple, reusable validation functions used across the project.
"""


def is_not_empty(value):
    """
    Return True if the value is not empty
    after removing leading and trailing spaces.
    """
    if value is None:
        return False

    return str(value).strip() != ""


def is_valid_email(email):
    """
    Basic email validation.

    Checks:
    - Email contains '@'
    - Local part is not empty
    - Domain part is not empty
    - Domain contains '.'

    This is a beginner-level validator and
    is not intended to validate every real-world
    email format.
    """

    if email is None:
        return False

    email = str(email).strip()

    if "@" not in email:
        return False

    local_part, _, domain_part = email.partition("@")

    if not local_part:
        return False

    if not domain_part:
        return False

    if "." not in domain_part:
        return False

    if domain_part.startswith("."):
        return False

    if domain_part.endswith("."):
        return False

    return True


def get_valid_text(prompt):
    """
    Keep asking the user until they enter
    a non-empty value.
    """

    while True:

        value = input(prompt).strip()

        if is_not_empty(value):
            return value

        print(
            "This field cannot be empty. "
            "Please try again."
        )


def get_valid_email(prompt):
    """
    Keep asking the user until they enter
    a valid-looking email address.
    """

    while True:

        value = input(prompt).strip()

        if is_valid_email(value):
            return value

        print(
            "Please enter a valid email address "
            "(e.g. name@example.com)."
        )


def id_exists(records, id_field, record_id):
    """
    Check whether a record with the given ID exists.

    ID comparison is case-insensitive.
    """

    if record_id is None:
        return False

    record_id = str(record_id).strip().lower()

    for record in records:

        existing_id = str(
            record.get(id_field, "")
        ).strip().lower()

        if existing_id == record_id:
            return True

    return False


def find_record_by_id(records, id_field, record_id):
    """
    Return the record with the given ID.

    Returns None if the record is not found.
    ID comparison is case-insensitive.
    """

    if record_id is None:
        return None

    record_id = str(record_id).strip().lower()

    for record in records:

        existing_id = str(
            record.get(id_field, "")
        ).strip().lower()

        if existing_id == record_id:
            return record

    return None