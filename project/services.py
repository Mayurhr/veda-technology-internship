"""
services.py

Handles all Service Management features:
Add, View, Search, Update, Delete digital services.
"""

import storage
import validation

FILENAME = "services.json"

DEFAULT_SERVICES = [
    {
        "service_id": "SVC001",
        "service_name": "Website Development",
        "category": "Web Services",
        "description": "Custom business website design and development",
        "status": "Active"
    },
    {
        "service_id": "SVC002",
        "service_name": "Cloud Hosting",
        "category": "Infrastructure",
        "description": "Managed cloud hosting and deployment services",
        "status": "Active"
    }
]


def load_services():
    return storage.load_data(FILENAME, DEFAULT_SERVICES)


def save_services(services):
    storage.save_data(FILENAME, services)


def add_service():
    services = load_services()

    print("\n--- Add New Service ---")
    service_name = validation.get_valid_text("Enter service name: ")
    category = validation.get_valid_text("Enter category: ")
    description = validation.get_valid_text("Enter description: ")
    status = validation.get_valid_text("Enter status (Active/Inactive): ")

    new_service = {
        "service_id": storage.generate_next_id(services, "service_id", "SVC"),
        "service_name": service_name,
        "category": category,
        "description": description,
        "status": status
    }

    services.append(new_service)
    save_services(services)

    print(f"Service added successfully with ID: {new_service['service_id']}")


def view_services():
    services = load_services()

    print("\n--- All Services ---")
    if not services:
        print("No services found.")
        return

    for service in services:
        print_service(service)


def print_service(service):
    print("-" * 40)
    print(f"ID          : {service['service_id']}")
    print(f"Name        : {service['service_name']}")
    print(f"Category    : {service['category']}")
    print(f"Description : {service['description']}")
    print(f"Status      : {service['status']}")


def search_services():
    services = load_services()

    print("\n--- Search Services ---")
    keyword = input("Enter category to search: ").strip().lower()

    results = [s for s in services if keyword in s["category"].lower()]

    if not results:
        print("No matching services found.")
        return

    print(f"\nFound {len(results)} matching service(s):")
    for service in results:
        print_service(service)


def update_service():
    services = load_services()

    print("\n--- Update Service ---")
    service_id = input("Enter Service ID to update: ").strip()

    service = validation.find_record_by_id(services, "service_id", service_id)
    if not service:
        print(f"No service found with ID: {service_id}")
        return

    print("Leave a field blank to keep its current value.")
    print_service(service)

    new_name = input(f"New name [{service['service_name']}]: ").strip()
    new_category = input(f"New category [{service['category']}]: ").strip()
    new_description = input(f"New description [{service['description']}]: ").strip()
    new_status = input(f"New status [{service['status']}]: ").strip()

    if new_name:
        service["service_name"] = new_name
    if new_category:
        service["category"] = new_category
    if new_description:
        service["description"] = new_description
    if new_status:
        service["status"] = new_status

    save_services(services)
    print("Service updated successfully.")


def delete_service():
    services = load_services()

    print("\n--- Delete Service ---")
    service_id = input("Enter Service ID to delete: ").strip()

    service = validation.find_record_by_id(services, "service_id", service_id)
    if not service:
        print(f"No service found with ID: {service_id}")
        return

    services.remove(service)
    save_services(services)
    print(f"Service {service_id} deleted successfully.")


def service_menu():
    while True:
        print("\n========================================")
        print("Service Management")
        print("========================================")
        print("1. Add Service")
        print("2. View Services")
        print("3. Search Services")
        print("4. Update Service")
        print("5. Delete Service")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_service()
        elif choice == "2":
            view_services()
        elif choice == "3":
            search_services()
        elif choice == "4":
            update_service()
        elif choice == "5":
            delete_service()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please select a valid option (1-6).")
