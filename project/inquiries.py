"""
inquiries.py

Handles Customer / Inquiry Management features:
Add, View, Search, Filter, Update, and Delete inquiries.
"""

import storage
import validation

FILENAME = "inquiries.json"

VALID_STATUSES = ["Open", "In Progress", "Closed"]

DEFAULT_INQUIRIES = [
    {
        "inquiry_id": "INQ001",
        "customer_name": "Rohan Sharma",
        "email": "rohan.sharma@example.com",
        "service": "Website Development",
        "message": "Interested in a business website with an admin panel.",
        "status": "Open"
    }
]


def load_inquiries():
    return storage.load_data(FILENAME, DEFAULT_INQUIRIES)


def save_inquiries(inquiries):
    storage.save_data(FILENAME, inquiries)


def add_inquiry():
    inquiries = load_inquiries()

    print("\n--- Add New Inquiry ---")

    customer_name = validation.get_valid_text("Enter customer name: ")
    email = validation.get_valid_email("Enter email: ")
    service = validation.get_valid_text("Enter service interested in: ")
    message = validation.get_valid_text("Enter inquiry message: ")

    new_inquiry = {
        "inquiry_id": storage.generate_next_id(
            inquiries,
            "inquiry_id",
            "INQ"
        ),
        "customer_name": customer_name,
        "email": email,
        "service": service,
        "message": message,
        "status": "Open"
    }

    inquiries.append(new_inquiry)
    save_inquiries(inquiries)

    print(
        f"Inquiry added successfully with ID: "
        f"{new_inquiry['inquiry_id']}"
    )


def view_inquiries():
    inquiries = load_inquiries()

    print("\n--- All Inquiries ---")

    if not inquiries:
        print("No inquiries found.")
        return

    for inquiry in inquiries:
        print_inquiry(inquiry)


def print_inquiry(inquiry):
    print("-" * 50)
    print(f"ID       : {inquiry.get('inquiry_id', '')}")
    print(f"Customer : {inquiry.get('customer_name', '')}")
    print(f"Email    : {inquiry.get('email', '')}")
    print(f"Service  : {inquiry.get('service', '')}")
    print(f"Message  : {inquiry.get('message', '')}")
    print(f"Status   : {inquiry.get('status', '')}")


def search_inquiries():
    inquiries = load_inquiries()

    print("\n--- Search Inquiries ---")

    keyword = input(
        "Enter customer name, email, or service: "
    ).strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = [
        inquiry
        for inquiry in inquiries
        if keyword in inquiry.get("customer_name", "").lower()
        or keyword in inquiry.get("email", "").lower()
        or keyword in inquiry.get("service", "").lower()
    ]

    if not results:
        print("No matching inquiries found.")
        return

    print(f"\nFound {len(results)} matching inquiry(ies):")

    for inquiry in results:
        print_inquiry(inquiry)


def filter_inquiries_by_status():
    inquiries = load_inquiries()

    print("\n--- Filter Inquiries by Status ---")

    print("Available statuses:")
    for index, status in enumerate(VALID_STATUSES, start=1):
        print(f"{index}. {status}")

    choice = input("Select status: ").strip()

    if choice not in ["1", "2", "3"]:
        print("Invalid status selection.")
        return

    selected_status = VALID_STATUSES[int(choice) - 1]

    results = [
        inquiry
        for inquiry in inquiries
        if inquiry.get("status") == selected_status
    ]

    if not results:
        print(f"No inquiries found with status: {selected_status}")
        return

    print(f"\n--- {selected_status} Inquiries ---")

    for inquiry in results:
        print_inquiry(inquiry)


def update_inquiry_status():
    inquiries = load_inquiries()

    print("\n--- Update Inquiry Status ---")

    inquiry_id = input(
        "Enter Inquiry ID to update: "
    ).strip().upper()

    inquiry = validation.find_record_by_id(
        inquiries,
        "inquiry_id",
        inquiry_id
    )

    if not inquiry:
        print(f"No inquiry found with ID: {inquiry_id}")
        return

    print_inquiry(inquiry)

    print("\nSelect new status:")

    for index, status in enumerate(VALID_STATUSES, start=1):
        print(f"{index}. {status}")

    choice = input("Enter choice: ").strip()

    if choice not in ["1", "2", "3"]:
        print("Invalid status selection.")
        return

    new_status = VALID_STATUSES[int(choice) - 1]

    inquiry["status"] = new_status

    save_inquiries(inquiries)

    print("Inquiry status updated successfully.")


def update_inquiry():
    inquiries = load_inquiries()

    print("\n--- Update Inquiry ---")

    inquiry_id = input(
        "Enter Inquiry ID to update: "
    ).strip().upper()

    inquiry = validation.find_record_by_id(
        inquiries,
        "inquiry_id",
        inquiry_id
    )

    if not inquiry:
        print(f"No inquiry found with ID: {inquiry_id}")
        return

    print("\nCurrent inquiry details:")
    print_inquiry(inquiry)

    print("\nEnter new details.")

    customer_name = validation.get_valid_text(
        "Enter customer name: "
    )

    email = validation.get_valid_email(
        "Enter email: "
    )

    service = validation.get_valid_text(
        "Enter service interested in: "
    )

    message = validation.get_valid_text(
        "Enter inquiry message: "
    )

    inquiry["customer_name"] = customer_name
    inquiry["email"] = email
    inquiry["service"] = service
    inquiry["message"] = message

    save_inquiries(inquiries)

    print("Inquiry updated successfully.")


def delete_inquiry():
    inquiries = load_inquiries()

    print("\n--- Delete Inquiry ---")

    inquiry_id = input(
        "Enter Inquiry ID to delete: "
    ).strip().upper()

    inquiry = validation.find_record_by_id(
        inquiries,
        "inquiry_id",
        inquiry_id
    )

    if not inquiry:
        print(f"No inquiry found with ID: {inquiry_id}")
        return

    print("\nInquiry to be deleted:")
    print_inquiry(inquiry)

    confirmation = input(
        "Are you sure you want to delete this inquiry? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Delete operation cancelled.")
        return

    inquiries.remove(inquiry)

    save_inquiries(inquiries)

    print("Inquiry deleted successfully.")


def inquiry_menu():
    while True:
        print("\n========================================")
        print("Customer / Inquiry Management")
        print("========================================")
        print("1. Add Inquiry")
        print("2. View Inquiries")
        print("3. Search Inquiries")
        print("4. Filter by Status")
        print("5. Update Inquiry")
        print("6. Update Inquiry Status")
        print("7. Delete Inquiry")
        print("8. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_inquiry()

        elif choice == "2":
            view_inquiries()

        elif choice == "3":
            search_inquiries()

        elif choice == "4":
            filter_inquiries_by_status()

        elif choice == "5":
            update_inquiry()

        elif choice == "6":
            update_inquiry_status()

        elif choice == "7":
            delete_inquiry()

        elif choice == "8":
            break

        else:
            print("Invalid choice. Please select a valid option (1-8).")