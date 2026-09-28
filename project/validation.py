"""
validation.py

Simple, reusable validation functions used across the project.
"""


def is_not_empty(value):
    """Return True if the value is not empty after trimming spaces."""
    return value.strip() != ""


def is_valid_email(email):
    """
    Very basic email validation.
    Checks for an '@' symbol and a '.' after it.
    Not a full real-world email validator, just beginner-level checking.
    """
    email = email.strip()
    if "@" not in email:
        return False

    local_part, _, domain_part = email.partition("@")
    if not local_part or not domain_part:
        return False

    if "." not in domain_part:
        return False

    return True


def get_valid_text(prompt):
    """Keep asking the user until they enter a non-empty value."""
    while True:
        value = input(prompt).strip()
        if is_not_empty(value):
            return value
        print("This field cannot be empty. Please try again.")


def get_valid_email(prompt):
    """Keep asking the user until they enter a valid-looking email."""
    while True:
        value = input(prompt).strip()
        if is_valid_email(value):
            return value
        print("Please enter a valid email address (e.g. name@example.com).")


def id_exists(records, id_field, record_id):
    """Check whether a record with the given ID already exists."""
    for record in records:
        if record[id_field].lower() == record_id.lower():
            return True
    return False


def find_record_by_id(records, id_field, record_id):
    """Return the record with the given ID, or None if not found."""
    for record in records:
        if record[id_field].lower() == record_id.lower():
            return record
    return None
