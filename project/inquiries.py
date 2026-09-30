"""
inquiries.py

Handles Customer / Inquiry Management:
Add, View, Search, Filter, Update, Update Status, and Delete.

Day 3:
Uses the Customer and Inquiry classes from models.py.
"""

import storage
import validation
from models import Customer, Inquiry


FILENAME = "inquiries.json"

VALID_STATUSES = [
    "Open",
    "In Progress",
    "Closed"
]


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
    """Load inquiries from JSON storage."""

    return storage.load_data(
        FILENAME,
        DEFAULT_INQUIRIES
    )


def save_inquiries(inquiries):
    """Save inquiries to JSON storage."""

    storage.save_data(
        FILENAME,
        inquiries
    )


def add_inquiry():
    """Add a new customer inquiry."""

    inquiries = load_inquiries()

    print("\n--- Add New Inquiry ---")

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

    print("\nAvailable statuses:")
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
            "Invalid status. "
            "Inquiry was not added."
        )
        return

    inquiry_id = storage.generate_next_id(
        inquiries,
        "inquiry_id",
        "INQ"
    )

    # Create Customer object
    customer = Customer(
        inquiry_id,
        customer_name,
        email
    )

    # Create Inquiry object
    inquiry = Inquiry(
        inquiry_id,
        customer.customer_name,
        customer.email,
        service,
        message,
        status
    )

    inquiries.append(
        inquiry.to_dict()
    )

    save_inquiries(inquiries)

    print(
        f"Inquiry added successfully "
        f"with ID: {inquiry_id}"
    )


def view_inquiries():
    """Display all customer inquiries."""

    inquiries = load_inquiries()

    print("\n--- All Inquiries ---")

    if not inquiries:
        print("No inquiries found.")
        return

    for inquiry in inquiries:
        print_inquiry(inquiry)


def print_inquiry(inquiry):
    """Display one inquiry."""

    print("-" * 50)

    print(
        f"ID       : "
        f"{inquiry.get('inquiry_id', '')}"
    )

    print(
        f"Customer : "
        f"{inquiry.get('customer_name', '')}"
    )

    print(
        f"Email    : "
        f"{inquiry.get('email', '')}"
    )

    print(
        f"Service  : "
        f"{inquiry.get('service', '')}"
    )

    print(
        f"Message  : "
        f"{inquiry.get('message', '')}"
    )

    print(
        f"Status   : "
        f"{inquiry.get('status', '')}"
    )


def search_inquiries():
    """Search inquiries by customer, email, or service."""

    inquiries = load_inquiries()

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
        for inquiry in inquiries
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
        print_inquiry(inquiry)


def filter_inquiries_by_status():
    """Filter inquiries by status."""

    inquiries = load_inquiries()

    print("\n--- Filter Inquiries by Status ---")
    print("1. Open")
    print("2. In Progress")
    print("3. Closed")

    choice = input(
        "Select status: "
    ).strip()

    if choice == "1":
        selected_status = "Open"

    elif choice == "2":
        selected_status = "In Progress"

    elif choice == "3":
        selected_status = "Closed"

    else:
        print(
            "Invalid status selection."
        )
        return

    results = [
        inquiry
        for inquiry in inquiries
        if inquiry.get("status") == selected_status
    ]

    if not results:
        print(
            f"No inquiries found with status: "
            f"{selected_status}"
        )
        return

    print(
        f"\n--- {selected_status} Inquiries ---"
    )

    for inquiry in results:
        print_inquiry(inquiry)


def update_inquiry():
    """Update an existing inquiry."""

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
        print(
            f"No inquiry found with ID: "
            f"{inquiry_id}"
        )
        return

    print("\nCurrent inquiry details:")
    print_inquiry(inquiry)

    print(
        "\nLeave a field blank to keep "
        "its current value."
    )

    new_customer = input(
        f"New customer name "
        f"[{inquiry['customer_name']}]: "
    ).strip()

    new_email = input(
        f"New email "
        f"[{inquiry['email']}]: "
    ).strip()

    new_service = input(
        f"New service "
        f"[{inquiry['service']}]: "
    ).strip()

    new_message = input(
        f"New message "
        f"[{inquiry['message']}]: "
    ).strip()

    print("\nStatus:")
    print("1. Open")
    print("2. In Progress")
    print("3. Closed")
    print("4. Keep current status")

    status_choice = input(
        "Select status: "
    ).strip()

    if status_choice not in [
        "",
        "1",
        "2",
        "3",
        "4"
    ]:
        print(
            "Invalid status selection."
        )
        return

    if new_customer:
        inquiry["customer_name"] = new_customer

    if new_email:
        if not validation.is_valid_email(
            new_email
        ):
            print(
                "Invalid email address. "
                "Inquiry was not updated."
            )
            return

        inquiry["email"] = new_email

    if new_service:
        inquiry["service"] = new_service

    if new_message:
        inquiry["message"] = new_message

    if status_choice == "1":
        inquiry["status"] = "Open"

    elif status_choice == "2":
        inquiry["status"] = "In Progress"

    elif status_choice == "3":
        inquiry["status"] = "Closed"

    save_inquiries(inquiries)

    print(
        "Inquiry updated successfully."
    )


def update_inquiry_status():
    """Update only the status of an inquiry."""

    inquiries = load_inquiries()

    print("\n--- Update Inquiry Status ---")

    inquiry_id = input(
        "Enter Inquiry ID: "
    ).strip().upper()

    inquiry = validation.find_record_by_id(
        inquiries,
        "inquiry_id",
        inquiry_id
    )

    if not inquiry:
        print(
            f"No inquiry found with ID: "
            f"{inquiry_id}"
        )
        return

    print("\nCurrent inquiry:")
    print_inquiry(inquiry)

    print("\nSelect new status:")
    print("1. Open")
    print("2. In Progress")
    print("3. Closed")

    choice = input(
        "Enter choice: "
    ).strip()

    if choice == "1":
        inquiry["status"] = "Open"

    elif choice == "2":
        inquiry["status"] = "In Progress"

    elif choice == "3":
        inquiry["status"] = "Closed"

    else:
        print(
            "Invalid status selection."
        )
        return

    save_inquiries(inquiries)

    print(
        "Inquiry status updated successfully."
    )


def delete_inquiry():
    """Delete an existing inquiry."""

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
        print(
            f"No inquiry found with ID: "
            f"{inquiry_id}"
        )
        return

    print("\nInquiry to be deleted:")
    print_inquiry(inquiry)

    confirmation = input(
        "Are you sure you want to delete "
        "this inquiry? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print(
            "Delete operation cancelled."
        )
        return

    inquiries.remove(inquiry)

    save_inquiries(inquiries)

    print(
        f"Inquiry {inquiry_id} "
        f"deleted successfully."
    )


def inquiry_menu():
    """Display the Customer / Inquiry Management menu."""

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

        choice = input(
            "Enter your choice: "
        ).strip()

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
            print(
                "Invalid choice. "
                "Please select a valid option (1-8)."
            )