"""
inquiries.py

Handles Customer / Inquiry Management features:
Add, View, Search, and Update inquiry status.
"""

import storage
import validation

FILENAME = "inquiries.json"

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
        "inquiry_id": storage.generate_next_id(inquiries, "inquiry_id", "INQ"),
        "customer_name": customer_name,
        "email": email,
        "service": service,
        "message": message,
        "status": "Open"
    }

    inquiries.append(new_inquiry)
    save_inquiries(inquiries)

    print(f"Inquiry added successfully with ID: {new_inquiry['inquiry_id']}")


def view_inquiries():
    inquiries = load_inquiries()

    print("\n--- All Inquiries ---")
    if not inquiries:
        print("No inquiries found.")
        return

    for inquiry in inquiries:
        print_inquiry(inquiry)


def print_inquiry(inquiry):
    print("-" * 40)
    print(f"ID       : {inquiry['inquiry_id']}")
    print(f"Customer : {inquiry['customer_name']}")
    print(f"Email    : {inquiry['email']}")
    print(f"Service  : {inquiry['service']}")
    print(f"Message  : {inquiry['message']}")
    print(f"Status   : {inquiry['status']}")


def search_inquiries():
    inquiries = load_inquiries()

    print("\n--- Search Inquiries ---")
    keyword = input("Enter customer name (or part of it) to search: ").strip().lower()

    results = [i for i in inquiries if keyword in i["customer_name"].lower()]

    if not results:
        print("No matching inquiries found.")
        return

    print(f"\nFound {len(results)} matching inquiry(ies):")
    for inquiry in results:
        print_inquiry(inquiry)


def update_inquiry_status():
    inquiries = load_inquiries()

    print("\n--- Update Inquiry Status ---")
    inquiry_id = input("Enter Inquiry ID to update: ").strip()

    inquiry = validation.find_record_by_id(inquiries, "inquiry_id", inquiry_id)
    if not inquiry:
        print(f"No inquiry found with ID: {inquiry_id}")
        return

    print_inquiry(inquiry)
    new_status = validation.get_valid_text(
        "Enter new status (Open/In Progress/Closed): "
    )
    inquiry["status"] = new_status

    save_inquiries(inquiries)
    print("Inquiry status updated successfully.")


def inquiry_menu():
    while True:
        print("\n========================================")
        print("Customer / Inquiry Management")
        print("========================================")
        print("1. Add Inquiry")
        print("2. View Inquiries")
        print("3. Search Inquiries")
        print("4. Update Inquiry Status")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_inquiry()
        elif choice == "2":
            view_inquiries()
        elif choice == "3":
            search_inquiries()
        elif choice == "4":
            update_inquiry_status()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please select a valid option (1-5).")
