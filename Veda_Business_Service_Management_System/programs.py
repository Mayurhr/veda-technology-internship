import storage
import validation


FILENAME = "programs.json"

VALID_STATUSES = [
    "Active",
    "Inactive"
]


DEFAULT_PROGRAMS = [
    {
        "program_id": "PRG001",
        "program_name": "Python Programming Internship",
        "category": "Software Development",
        "duration": "4 Days",
        "status": "Active"
    },
    {
        "program_id": "PRG002",
        "program_name": "Full Stack Web Development",
        "category": "Software Development",
        "duration": "6 Weeks",
        "status": "Active"
    },
    {
        "program_id": "PRG003",
        "program_name": "Cloud DevOps Bootcamp",
        "category": "Cloud Computing",
        "duration": "3 Weeks",
        "status": "Active"
    }
]


def load_programs():
    """Load programs from JSON storage."""

    return storage.load_data(
        FILENAME,
        DEFAULT_PROGRAMS
    )


def save_programs(programs):
    """Save programs to JSON storage."""

    return storage.save_data(
        FILENAME,
        programs
    )


def add_program():
    """Add a new program."""

    programs = load_programs()

    print("\n--- Add New Program ---")

    program_name = validation.get_valid_text(
        "Enter program name: "
    )

    category = validation.get_valid_text(
        "Enter category: "
    )

    duration = validation.get_valid_text(
        "Enter duration: "
    )

    print("\nAvailable statuses:")
    print("1. Active")
    print("2. Inactive")

    status_choice = input(
        "Select status: "
    ).strip()

    if status_choice == "1":
        status = "Active"

    elif status_choice == "2":
        status = "Inactive"

    else:
        print(
            "Invalid status. "
            "Program was not added."
        )
        return

    program_id = storage.generate_next_id(
        programs,
        "PRG",
        "program_id"
    )

    new_program = {
        "program_id": program_id,
        "program_name": program_name,
        "category": category,
        "duration": duration,
        "status": status
    }

    programs.append(new_program)

    if not save_programs(programs):
        print("Could not save changes.")
        return

    print(
        f"Program added successfully "
        f"with ID: {program_id}"
    )


def view_programs():
    """Display all programs."""

    programs = load_programs()

    print("\n--- All Programs ---")

    if not programs:
        print("No programs found.")
        return

    for program in programs:
        print_program(program)


def print_program(program):
    """Display one program."""

    print("-" * 40)

    print(
        f"ID       : "
        f"{program.get('program_id', '')}"
    )

    print(
        f"Name     : "
        f"{program.get('program_name', '')}"
    )

    print(
        f"Category : "
        f"{program.get('category', '')}"
    )

    print(
        f"Duration : "
        f"{program.get('duration', '')}"
    )

    print(
        f"Status   : "
        f"{program.get('status', '')}"
    )


def search_programs():
    """Search programs by name or category."""

    programs = load_programs()

    print("\n--- Search Programs ---")

    keyword = input(
        "Enter program name or category: "
    ).strip().lower()

    if not keyword:
        print(
            "Search keyword cannot be empty."
        )
        return

    results = [
        program
        for program in programs
        if keyword in program.get(
            "program_name",
            ""
        ).lower()
        or keyword in program.get(
            "category",
            ""
        ).lower()
    ]

    if not results:
        print(
            "No matching programs found."
        )
        return

    print(
        f"\nFound {len(results)} "
        f"matching program(s):"
    )

    for program in results:
        print_program(program)


def filter_programs_by_status():
    """Filter programs by Active or Inactive status."""

    programs = load_programs()

    print("\n--- Filter Programs by Status ---")
    print("1. Active")
    print("2. Inactive")

    choice = input(
        "Select status: "
    ).strip()

    if choice == "1":
        selected_status = "Active"

    elif choice == "2":
        selected_status = "Inactive"

    else:
        print(
            "Invalid status selection."
        )
        return

    results = [
        program
        for program in programs
        if program.get("status") == selected_status
    ]

    if not results:
        print(
            f"No programs found with status: "
            f"{selected_status}"
        )
        return

    print(
        f"\n--- {selected_status} Programs ---"
    )

    for program in results:
        print_program(program)


def update_program():
    """Update an existing program."""

    programs = load_programs()

    print("\n--- Update Program ---")

    program_id = input(
        "Enter Program ID to update: "
    ).strip().upper()

    program = validation.find_record_by_id(
        programs,
        "program_id",
        program_id
    )

    if not program:
        print(
            f"No program found with ID: "
            f"{program_id}"
        )
        return

    print("\nCurrent program details:")
    print_program(program)

    print(
        "\nLeave a field blank to keep "
        "its current value."
    )

    new_name = input(
        f"New name [{program.get('program_name', '')}]: "
    ).strip()

    new_category = input(
        f"New category [{program.get('category', '')}]: "
    ).strip()

    new_duration = input(
        f"New duration [{program.get('duration', '')}]: "
    ).strip()

    print("\nStatus:")
    print("1. Active")
    print("2. Inactive")
    print("3. Keep current status")

    status_choice = input(
        "Select status: "
    ).strip()

    if status_choice not in [
        "",
        "1",
        "2",
        "3"
    ]:
        print(
            "Invalid status selection."
        )
        return

    if new_name:
        program["program_name"] = new_name

    if new_category:
        program["category"] = new_category

    if new_duration:
        program["duration"] = new_duration

    if status_choice == "1":
        program["status"] = "Active"

    elif status_choice == "2":
        program["status"] = "Inactive"

    if not save_programs(programs):
        print("Could not save changes.")
        return

    print(
        "Program updated successfully."
    )


def delete_program():
    """Delete an existing program."""

    programs = load_programs()

    print("\n--- Delete Program ---")

    program_id = input(
        "Enter Program ID to delete: "
    ).strip().upper()

    program = validation.find_record_by_id(
        programs,
        "program_id",
        program_id
    )

    if not program:
        print(
            f"No program found with ID: "
            f"{program_id}"
        )
        return

    print("\nProgram to be deleted:")
    print_program(program)

    confirmation = input(
        "Are you sure you want to delete "
        "this program? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print(
            "Delete operation cancelled."
        )
        return

    programs.remove(program)

    if not save_programs(programs):
        print("Could not save changes.")
        return

    print(
        f"Program {program_id} "
        f"deleted successfully."
    )


def program_menu():
    """Display the Program Management menu."""

    while True:

        print("\n========================================")
        print("Program Management")
        print("========================================")
        print("1. Add Program")
        print("2. View Programs")
        print("3. Search Programs")
        print("4. Filter by Status")
        print("5. Update Program")
        print("6. Delete Program")
        print("7. Back to Main Menu")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            add_program()

        elif choice == "2":
            view_programs()

        elif choice == "3":
            search_programs()

        elif choice == "4":
            filter_programs_by_status()

        elif choice == "5":
            update_program()

        elif choice == "6":
            delete_program()

        elif choice == "7":
            break

        else:
            print(
                "Invalid choice. "
                "Please select a valid option (1-7)."
            )