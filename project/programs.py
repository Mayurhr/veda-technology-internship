"""
programs.py

Handles all Program Management features:
Add, View, Search, Update, Delete programs.
"""

import storage
import validation

FILENAME = "programs.json"

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
    }
]


def load_programs():
    return storage.load_data(FILENAME, DEFAULT_PROGRAMS)


def save_programs(programs):
    storage.save_data(FILENAME, programs)


def add_program():
    programs = load_programs()

    print("\n--- Add New Program ---")
    program_name = validation.get_valid_text("Enter program name: ")
    category = validation.get_valid_text("Enter category: ")
    duration = validation.get_valid_text("Enter duration: ")
    status = validation.get_valid_text("Enter status (Active/Inactive): ")

    new_program = {
        "program_id": storage.generate_next_id(programs, "program_id", "PRG"),
        "program_name": program_name,
        "category": category,
        "duration": duration,
        "status": status
    }

    programs.append(new_program)
    save_programs(programs)

    print(f"Program added successfully with ID: {new_program['program_id']}")


def view_programs():
    programs = load_programs()

    print("\n--- All Programs ---")
    if not programs:
        print("No programs found.")
        return

    for program in programs:
        print_program(program)


def print_program(program):
    print("-" * 40)
    print(f"ID       : {program['program_id']}")
    print(f"Name     : {program['program_name']}")
    print(f"Category : {program['category']}")
    print(f"Duration : {program['duration']}")
    print(f"Status   : {program['status']}")


def search_programs():
    programs = load_programs()

    print("\n--- Search Programs ---")
    keyword = input("Enter program name (or part of it) to search: ").strip().lower()

    results = [p for p in programs if keyword in p["program_name"].lower()]

    if not results:
        print("No matching programs found.")
        return

    print(f"\nFound {len(results)} matching program(s):")
    for program in results:
        print_program(program)


def update_program():
    programs = load_programs()

    print("\n--- Update Program ---")
    program_id = input("Enter Program ID to update: ").strip()

    program = validation.find_record_by_id(programs, "program_id", program_id)
    if not program:
        print(f"No program found with ID: {program_id}")
        return

    print("Leave a field blank to keep its current value.")
    print_program(program)

    new_name = input(f"New name [{program['program_name']}]: ").strip()
    new_category = input(f"New category [{program['category']}]: ").strip()
    new_duration = input(f"New duration [{program['duration']}]: ").strip()
    new_status = input(f"New status [{program['status']}]: ").strip()

    if new_name:
        program["program_name"] = new_name
    if new_category:
        program["category"] = new_category
    if new_duration:
        program["duration"] = new_duration
    if new_status:
        program["status"] = new_status

    save_programs(programs)
    print("Program updated successfully.")


def delete_program():
    programs = load_programs()

    print("\n--- Delete Program ---")
    program_id = input("Enter Program ID to delete: ").strip()

    program = validation.find_record_by_id(programs, "program_id", program_id)
    if not program:
        print(f"No program found with ID: {program_id}")
        return

    programs.remove(program)
    save_programs(programs)
    print(f"Program {program_id} deleted successfully.")


def program_menu():
    while True:
        print("\n========================================")
        print("Program Management")
        print("========================================")
        print("1. Add Program")
        print("2. View Programs")
        print("3. Search Programs")
        print("4. Update Program")
        print("5. Delete Program")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_program()
        elif choice == "2":
            view_programs()
        elif choice == "3":
            search_programs()
        elif choice == "4":
            update_program()
        elif choice == "5":
            delete_program()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please select a valid option (1-6).")
