"""
search.py

Provides a combined Search menu that lets the user search
programs, services, and inquiries, or filter records by status.
"""

import programs
import services
import inquiries


def filter_by_status():
    print("\n--- Filter Records by Status ---")
    print("1. Programs")
    print("2. Services")
    print("3. Inquiries")

    choice = input(
        "Choose what to filter (1-3): "
    ).strip()

    if choice not in ("1", "2", "3"):
        print("Invalid choice.")
        return

    print("\nAvailable status examples:")
    print("Active / Inactive")
    print("Open / In Progress / Closed")

    status = input(
        "Enter status to filter by: "
    ).strip().lower()

    if not status:
        print("Status cannot be empty.")
        return

    if choice == "1":
        records = programs.load_programs()

        results = [
            record
            for record in records
            if record.get("status", "").lower() == status
        ]

        if not results:
            print("No programs found with that status.")
            return

        print(f"\n--- Programs with status: {status.title()} ---")

        for record in results:
            programs.print_program(record)

    elif choice == "2":
        records = services.load_services()

        results = [
            record
            for record in records
            if record.get("status", "").lower() == status
        ]

        if not results:
            print("No services found with that status.")
            return

        print(f"\n--- Services with status: {status.title()} ---")

        for record in results:
            services.print_service(record)

    elif choice == "3":
        records = inquiries.load_inquiries()

        results = [
            record
            for record in records
            if record.get("status", "").lower() == status
        ]

        if not results:
            print("No inquiries found with that status.")
            return

        print(f"\n--- Inquiries with status: {status.title()} ---")

        for record in results:
            inquiries.print_inquiry(record)


def search_programs_by_category():
    programs_list = programs.load_programs()

    print("\n--- Search Programs by Category ---")

    keyword = input(
        "Enter category (or part of it): "
    ).strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = [
        program
        for program in programs_list
        if keyword in program.get("category", "").lower()
    ]

    if not results:
        print("No programs found in that category.")
        return

    print(f"\nFound {len(results)} matching program(s):")

    for program in results:
        programs.print_program(program)


def search_services_by_name():
    services_list = services.load_services()

    print("\n--- Search Services by Name ---")

    keyword = input(
        "Enter service name (or part of it): "
    ).strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = [
        service
        for service in services_list
        if keyword in service.get("service_name", "").lower()
    ]

    if not results:
        print("No matching services found.")
        return

    print(f"\nFound {len(results)} matching service(s):")

    for service in results:
        services.print_service(service)


def search_menu():
    while True:
        print("\n========================================")
        print("Search and Filtering")
        print("========================================")
        print("1. Search Programs by Name or Category")
        print("2. Search Programs by Category")
        print("3. Search Services by Category")
        print("4. Search Services by Name")
        print("5. Search Inquiries by Customer, Email or Service")
        print("6. Filter Records by Status")
        print("7. Back to Main Menu")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            programs.search_programs()

        elif choice == "2":
            search_programs_by_category()

        elif choice == "3":
            services.search_services()

        elif choice == "4":
            search_services_by_name()

        elif choice == "5":
            inquiries.search_inquiries()

        elif choice == "6":
            filter_by_status()

        elif choice == "7":
            break

        else:
            print(
                "Invalid choice. "
                "Please select a valid option (1-7)."
            )