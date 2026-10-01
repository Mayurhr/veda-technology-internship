import programs
import services
import inquiries


def count_by_status(records, status):
    count = 0

    for record in records:
        if str(record.get("status", "")).strip().lower() == status.lower():
            count += 1

    return count


def count_by_field(records, field):
    """Count records grouped by a selected field."""

    counts = {}

    for record in records:
        value = record.get(field, "Unknown")

        if not value:
            value = "Unknown"

        counts[value] = counts.get(value, 0) + 1

    return counts


def display_counts(title, counts):
    """Display grouped count information."""

    print(f"\n--- {title} ---")

    if not counts:
        print("No data found.")
        return

    for key, value in counts.items():
        print(f"{key}: {value}")


def show_business_summary():
    """Display an overall business summary."""

    program_data = programs.load_programs()
    service_data = services.load_services()
    inquiry_data = inquiries.load_inquiries()

    print("\n========================================")
    print("Business Summary Report")
    print("========================================")

    print(f"Total Programs : {len(program_data)}")
    print(f"Total Services : {len(service_data)}")
    print(f"Total Inquiries: {len(inquiry_data)}")

    print("\nProgram Status")
    print(
        f"Active   : "
        f"{count_by_status(program_data, 'Active')}"
    )
    print(
        f"Inactive : "
        f"{count_by_status(program_data, 'Inactive')}"
    )

    print("\nService Status")
    print(
        f"Active   : "
        f"{count_by_status(service_data, 'Active')}"
    )
    print(
        f"Inactive : "
        f"{count_by_status(service_data, 'Inactive')}"
    )

    print("\nInquiry Status")
    print(
        f"Open        : "
        f"{count_by_status(inquiry_data, 'Open')}"
    )
    print(
        f"In Progress : "
        f"{count_by_status(inquiry_data, 'In Progress')}"
    )
    print(
        f"Closed      : "
        f"{count_by_status(inquiry_data, 'Closed')}"
    )


def show_category_reports():
    """Display programs and services grouped by category."""

    program_data = programs.load_programs()
    service_data = services.load_services()

    program_categories = count_by_field(
        program_data,
        "category"
    )

    service_categories = count_by_field(
        service_data,
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

    inquiry_data = inquiries.load_inquiries()

    status_counts = count_by_field(
        inquiry_data,
        "status"
    )

    display_counts(
        "Inquiries by Status",
        status_counts
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
        print("4. Back to Main Menu")

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
            break

        else:
            print(
                "Invalid choice. "
                "Please select a valid option (1-4)."
            )