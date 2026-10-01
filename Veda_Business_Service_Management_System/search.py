"""
search.py

Provides combined search and filtering
across programs, services, and inquiries.

Day 3:
Works with the updated Program, Service,
Customer, and Inquiry management modules.
"""

import programs
import services
import inquiries


def search_programs_by_name_or_category():
    """Search programs by name or category."""

    program_list = programs.load_programs()

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
        for program in program_list
        if keyword in program.get(
            "program_name", ""
        ).lower()
        or keyword in program.get(
            "category", ""
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
        programs.print_program(program)


def search_programs_by_category():
    """Search programs by category."""

    program_list = programs.load_programs()

    print("\n--- Search Programs by Category ---")

    category = input(
        "Enter category: "
    ).strip().lower()

    if not category:
        print(
            "Category cannot be empty."
        )
        return

    results = [
        program
        for program in program_list
        if category in program.get(
            "category", ""
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
        programs.print_program(program)


def search_services_by_name_or_category():
    """Search services by name or category."""

    service_list = services.load_services()

    print("\n--- Search Services ---")

    keyword = input(
        "Enter service name or category: "
    ).strip().lower()

    if not keyword:
        print(
            "Search keyword cannot be empty."
        )
        return

    results = [
        service
        for service in service_list
        if keyword in service.get(
            "service_name", ""
        ).lower()
        or keyword in service.get(
            "category", ""
        ).lower()
    ]

    if not results:
        print(
            "No matching services found."
        )
        return

    print(
        f"\nFound {len(results)} "
        f"matching service(s):"
    )

    for service in results:
        services.print_service(service)


def search_services_by_category():
    """Search services by category."""

    service_list = services.load_services()

    print("\n--- Search Services by Category ---")

    category = input(
        "Enter category: "
    ).strip().lower()

    if not category:
        print(
            "Category cannot be empty."
        )
        return

    results = [
        service
        for service in service_list
        if category in service.get(
            "category", ""
        ).lower()
    ]

    if not results:
        print(
            "No matching services found."
        )
        return

    print(
        f"\nFound {len(results)} "
        f"matching service(s):"
    )

    for service in results:
        services.print_service(service)


def search_inquiries():
    """Search inquiries by customer, email, or service."""

    inquiry_list = inquiries.load_inquiries()

    print("\n--- Search Inquiries ---")

    keyword = input(
        "Enter customer name, email or service: "
    ).strip().lower()

    if not keyword:
        print(
            "Search keyword cannot be empty."
        )
        return

    results = [
        inquiry
        for inquiry in inquiry_list
        if keyword in inquiry.get(
            "customer_name", ""
        ).lower()
        or keyword in inquiry.get(
            "email", ""
        ).lower()
        or keyword in inquiry.get(
            "service", ""
        ).lower()
    ]

    if not results:
        print(
            "No matching inquiries found."
        )
        return

    print(
        f"\nFound {len(results)} "
        f"matching inquiry(ies):"
    )

    for inquiry in results:
        inquiries.print_inquiry(inquiry)


def filter_records_by_status():
    """Filter programs, services, or inquiries by status."""

    print("\n--- Filter Records by Status ---")
    print("1. Programs")
    print("2. Services")
    print("3. Inquiries")

    record_choice = input(
        "Select record type: "
    ).strip()

    if record_choice == "1":

        print("\nProgram Status:")
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
                "Invalid status selection."
            )
            return

        records = programs.load_programs()

        results = [
            program
            for program in records
            if program.get("status") == status
        ]

        if not results:
            print(
                f"No programs found with "
                f"status: {status}"
            )
            return

        print(
            f"\n--- {status} Programs ---"
        )

        for program in results:
            programs.print_program(program)

    elif record_choice == "2":

        print("\nService Status:")
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
                "Invalid status selection."
            )
            return

        records = services.load_services()

        results = [
            service
            for service in records
            if service.get("status") == status
        ]

        if not results:
            print(
                f"No services found with "
                f"status: {status}"
            )
            return

        print(
            f"\n--- {status} Services ---"
        )

        for service in results:
            services.print_service(service)

    elif record_choice == "3":

        print("\nInquiry Status:")
        print("1. Open")
        print("2. In Progress")
        print("3. Closed")

        status_choice = input(
            "Select status: "
        ).strip()

        if status_choice == "1":
            status = "Open"

        elif status_choice == "2":
            status = "In Progress"

        elif status_choice == "3":
            status = "Closed"

        else:
            print(
                "Invalid status selection."
            )
            return

        records = inquiries.load_inquiries()

        results = [
            inquiry
            for inquiry in records
            if inquiry.get("status") == status
        ]

        if not results:
            print(
                f"No inquiries found with "
                f"status: {status}"
            )
            return

        print(
            f"\n--- {status} Inquiries ---"
        )

        for inquiry in results:
            inquiries.print_inquiry(inquiry)

    else:
        print(
            "Invalid record type selection."
        )


def search_menu():
    """Display the combined Search menu."""

    while True:

        print("\n========================================")
        print("Search")
        print("========================================")
        print("1. Search Programs by Name or Category")
        print("2. Search Programs by Category")
        print("3. Search Services by Name or Category")
        print("4. Search Services by Category")
        print("5. Search Inquiries")
        print("6. Filter Records by Status")
        print("7. Back to Main Menu")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            search_programs_by_name_or_category()

        elif choice == "2":
            search_programs_by_category()

        elif choice == "3":
            search_services_by_name_or_category()

        elif choice == "4":
            search_services_by_category()

        elif choice == "5":
            search_inquiries()

        elif choice == "6":
            filter_records_by_status()

        elif choice == "7":
            break

        else:
            print(
                "Invalid choice. "
                "Please select a valid option (1-7)."
            )