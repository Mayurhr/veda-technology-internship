"""
reports.py

Provides business reports for:
- Programs
- Services
- Customer inquiries

Day 3:
Adds simple reporting and summary features.
"""

import programs
import services
import inquiries


def count_by_status(records, status):
    """Count records matching a specific status."""

    return sum(
        1
        for record in records
        if record.get("status", "").lower()
        == status.lower()
    )


def count_by_field(records, field):
    """Count records grouped by a specific field."""

    counts = {}

    for record in records:

        value = record.get(
            field,
            "Unknown"
        )

        if not value:
            value = "Unknown"

        counts[value] = (
            counts.get(value, 0) + 1
        )

    return counts


def display_counts(title, counts):
    """Display grouped counts."""

    print(f"\n--- {title} ---")

    if not counts:
        print("No data found.")
        return

    for key, value in counts.items():
        print(f"{key}: {value}")


def show_business_summary():
    """Display overall business summary."""

    program_list = programs.load_programs()
    service_list = services.load_services()
    inquiry_list = inquiries.load_inquiries()

    print("\n========================================")
    print("Business Summary Report")
    print("========================================")

    print(
        f"Total Programs : "
        f"{len(program_list)}"
    )

    print(
        f"Total Services : "
        f"{len(service_list)}"
    )

    print(
        f"Total Inquiries: "
        f"{len(inquiry_list)}"
    )

    print("\nProgram Status")

    print(
        f"Active   : "
        f"{count_by_status(program_list, 'Active')}"
    )

    print(
        f"Inactive : "
        f"{count_by_status(program_list, 'Inactive')}"
    )

    print("\nService Status")

    print(
        f"Active   : "
        f"{count_by_status(service_list, 'Active')}"
    )

    print(
        f"Inactive : "
        f"{count_by_status(service_list, 'Inactive')}"
    )

    print("\nInquiry Status")

    print(
        f"Open        : "
        f"{count_by_status(inquiry_list, 'Open')}"
    )

    print(
        f"In Progress : "
        f"{count_by_status(inquiry_list, 'In Progress')}"
    )

    print(
        f"Closed      : "
        f"{count_by_status(inquiry_list, 'Closed')}"
    )


def show_category_reports():
    """Display programs and services grouped by category."""

    program_list = programs.load_programs()
    service_list = services.load_services()

    program_categories = count_by_field(
        program_list,
        "category"
    )

    service_categories = count_by_field(
        service_list,
        "category"
    )

    display_counts(
        "Programs by Category",
        program_categories
    )

    display_counts(
        "Services by Category",
        service_categories
    )


def show_inquiry_status_report():
    """Display inquiries grouped by status."""

    inquiry_list = inquiries.load_inquiries()

    status_counts = count_by_field(
        inquiry_list,
        "status"
    )

    display_counts(
        "Inquiries by Status",
        status_counts
    )


def show_program_report():
    """Display detailed program report."""

    program_list = programs.load_programs()

    print("\n========================================")
    print("Program Report")
    print("========================================")

    print(
        f"Total Programs: "
        f"{len(program_list)}"
    )

    print(
        f"Active Programs: "
        f"{count_by_status(program_list, 'Active')}"
    )

    print(
        f"Inactive Programs: "
        f"{count_by_status(program_list, 'Inactive')}"
    )

    display_counts(
        "Programs by Category",
        count_by_field(
            program_list,
            "category"
        )
    )


def show_service_report():
    """Display detailed service report."""

    service_list = services.load_services()

    print("\n========================================")
    print("Service Report")
    print("========================================")

    print(
        f"Total Services: "
        f"{len(service_list)}"
    )

    print(
        f"Active Services: "
        f"{count_by_status(service_list, 'Active')}"
    )

    print(
        f"Inactive Services: "
        f"{count_by_status(service_list, 'Inactive')}"
    )

    display_counts(
        "Services by Category",
        count_by_field(
            service_list,
            "category"
        )
    )


def report_menu():
    """Display the Business Reports menu."""

    while True:

        print("\n========================================")
        print("Business Reports")
        print("========================================")
        print("1. Business Summary")
        print("2. Category Reports")
        print("3. Inquiry Status Report")
        print("4. Program Report")
        print("5. Service Report")
        print("6. Back to Main Menu")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            show_business_summary()

        elif choice == "2":
            show_category_reports()

        elif choice == "3":
            show_inquiry_status_report()

        elif choice == "4":
            show_program_report()

        elif choice == "5":
            show_service_report()

        elif choice == "6":
            break

        else:
            print(
                "Invalid choice. "
                "Please select a valid option (1-6)."
            )