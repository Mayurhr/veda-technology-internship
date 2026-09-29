"""
services.py

Handles all Service Management features:
Add, View, Search, Filter, Update, and Delete digital services.
"""

import storage
import validation

FILENAME = "services.json"

VALID_STATUSES = ["Active", "Inactive"]

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

    service_name = validation.get_valid_text(
        "Enter service name: "
    )

    category = validation.get_valid_text(
        "Enter category: "
    )

    description = validation.get_valid_text(
        "Enter description: "
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
        print("Invalid status. Service was not added.")
        return

    new_service = {
        "service_id": storage.generate_next_id(
            services,
            "service_id",
            "SVC"
        ),
        "service_name": service_name,
        "category": category,
        "description": description,
        "status": status
    }

    services.append(new_service)
    save_services(services)

    print(
        f"Service added successfully with ID: "
        f"{new_service['service_id']}"
    )


def view_services():
    services = load_services()

    print("\n--- All Services ---")

    if not services:
        print("No services found.")
        return

    for service in services:
        print_service(service)


def print_service(service):
    print("-" * 50)
    print(f"ID          : {service.get('service_id', '')}")
    print(f"Name        : {service.get('service_name', '')}")
    print(f"Category    : {service.get('category', '')}")
    print(f"Description : {service.get('description', '')}")
    print(f"Status      : {service.get('status', '')}")


def search_services():
    services = load_services()

    print("\n--- Search Services ---")

    keyword = input(
        "Enter service name or category: "
    ).strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = [
        service
        for service in services
        if keyword in service.get("service_name", "").lower()
        or keyword in service.get("category", "").lower()
    ]

    if not results:
        print("No matching services found.")
        return

    print(f"\nFound {len(results)} matching service(s):")

    for service in results:
        print_service(service)


def filter_services_by_status():
    services = load_services()

    print("\n--- Filter Services by Status ---")
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
        print("Invalid status selection.")
        return

    results = [
        service
        for service in services
        if service.get("status") == selected_status
    ]

    if not results:
        print(
            f"No services found with status: "
            f"{selected_status}"
        )
        return

    print(
        f"\n--- {selected_status} Services ---"
    )

    for service in results:
        print_service(service)


def update_service():
    services = load_services()

    print("\n--- Update Service ---")

    service_id = input(
        "Enter Service ID to update: "
    ).strip().upper()

    service = validation.find_record_by_id(
        services,
        "service_id",
        service_id
    )

    if not service:
        print(
            f"No service found with ID: "
            f"{service_id}"
        )
        return

    print("\nCurrent service details:")
    print_service(service)

    print(
        "\nLeave a field blank to keep "
        "its current value."
    )

    new_name = input(
        f"New name [{service['service_name']}]: "
    ).strip()

    new_category = input(
        f"New category [{service['category']}]: "
    ).strip()

    new_description = input(
        f"New description [{service['description']}]: "
    ).strip()

    print("\nStatus:")
    print("1. Active")
    print("2. Inactive")
    print("3. Keep current status")

    status_choice = input(
        "Select status: "
    ).strip()

    if new_name:
        service["service_name"] = new_name

    if new_category:
        service["category"] = new_category

    if new_description:
        service["description"] = new_description

    if status_choice == "1":
        service["status"] = "Active"

    elif status_choice == "2":
        service["status"] = "Inactive"

    elif status_choice == "3" or status_choice == "":
        pass

    else:
        print("Invalid status selection.")
        return

    save_services(services)

    print("Service updated successfully.")


def delete_service():
    services = load_services()

    print("\n--- Delete Service ---")

    service_id = input(
        "Enter Service ID to delete: "
    ).strip().upper()

    service = validation.find_record_by_id(
        services,
        "service_id",
        service_id
    )

    if not service:
        print(
            f"No service found with ID: "
            f"{service_id}"
        )
        return

    print("\nService to be deleted:")
    print_service(service)

    confirmation = input(
        "Are you sure you want to delete this service? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Delete operation cancelled.")
        return

    services.remove(service)

    save_services(services)

    print(
        f"Service {service_id} deleted successfully."
    )


def service_menu():
    while True:
        print("\n========================================")
        print("Service Management")
        print("========================================")
        print("1. Add Service")
        print("2. View Services")
        print("3. Search Services")
        print("4. Filter by Status")
        print("5. Update Service")
        print("6. Delete Service")
        print("7. Back to Main Menu")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            add_service()

        elif choice == "2":
            view_services()

        elif choice == "3":
            search_services()

        elif choice == "4":
            filter_services_by_status()

        elif choice == "5":
            update_service()

        elif choice == "6":
            delete_service()

        elif choice == "7":
            break

        else:
            print(
                "Invalid choice. "
                "Please select a valid option (1-7)."
            )