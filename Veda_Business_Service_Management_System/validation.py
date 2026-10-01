def is_not_empty(value):
    """
    Check whether a value is not empty.
    """

    if value is None:
        return False

    return bool(str(value).strip())


def is_valid_email(email):
    """
    Perform basic email validation.
    """

    if not is_not_empty(email):
        return False

    email = str(email).strip()

    if "@" not in email:
        return False

    if "." not in email.split("@")[-1]:
        return False

    if email.startswith("@") or email.endswith("@"):
        return False

    return True


def get_valid_text(prompt):
    """
    Get non-empty text input from the user.
    """

    while True:

        value = input(prompt).strip()

        if is_not_empty(value):
            return value

        print("Input cannot be empty. Please try again.")


def get_valid_email(prompt):
    """
    Get a valid email address from the user.
    """

    while True:

        email = input(prompt).strip()

        if is_valid_email(email):
            return email

        print("Invalid email address. Please try again.")


def id_exists(records, field, record_id):
    """
    Check whether an ID already exists.

    Comparison is case-insensitive.
    """

    if not record_id:
        return False

    record_id = str(record_id).strip().lower()

    for record in records:

        existing_id = str(
            record.get(field, "")
        ).strip().lower()

        if existing_id == record_id:
            return True

    return False


def find_record_by_id(records, field, record_id):
    """
    Find and return a record by ID.

    Returns None if the record is not found.
    """

    if not record_id:
        return None

    record_id = str(record_id).strip().lower()

    for record in records:

        existing_id = str(
            record.get(field, "")
        ).strip().lower()

        if existing_id == record_id:
            return record

    return None


def is_valid_status(status, valid_statuses):
    """
    Check whether a status belongs to
    the allowed status list.
    """

    if not is_not_empty(status):
        return False

    return str(status).strip().lower() in [
        str(value).strip().lower()
        for value in valid_statuses
    ]


def get_valid_status(prompt, valid_statuses):
    """
    Get a valid status from the user.
    """

    while True:

        status = input(prompt).strip()

        if is_valid_status(
            status,
            valid_statuses
        ):
            return status

        print(
            "Invalid status. Choose from: "
            + ", ".join(valid_statuses)
        )