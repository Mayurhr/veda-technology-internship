"""
services.py

Handles all Service Management features:
Add, View, Search, Filter, Update, and Delete digital services.
"""

import storage
import validation


FILENAME = "services.json"

VALID_STATUSES = [
    "Active",
    "Inactive"
]


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
    },
    {
        "service_id": "SVC003",
        "service_name": "Mobile App Development",
        "category": "Mobile Services",
        "description": "Custom Android and iOS app development for startups",
        "status": "Active"
    }
]


def load_services():
    """Load services from JSON storage."""

    return storage.load_data(
        FILENAME,
        DEFAULT_SERVICES
    )


def save_services(services):
    """Save services to JSON storage."""

    return storage.save_data(
        FILENAME,
        services
    )


def add_service():
    """Add a new service."""

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
        print(
            "Invalid status. "
            "Service was not added."
        )
        return

    service_id = storage.generate_next_id(
        services,
        "SVC",
        "service_id"
    )

    new_service = {
        "service_id": service_id,
        "service_name": service_name,
        "category": category,
        "description": description,
        "status": status
    }

    services.append(new_service)

    if not save_services(services):
        print("Could not save changes.")
        return

    print(
        f"Service added successfully "
        f"with ID: {service_id}"
    )


def view_services():
    """Display all services."""

    services = load_services()

    print("\n--- All Services ---")

    if not services:
        print("No services found.")
        return

    for service in services:
        print_service(service)


def print_service(service):
    """Display one service."""

    print("-" * 50)

    print(
        f"ID          : "
        f"{service.get('service_id', '')}"
    )

    print(
        f"Name        : "
        f"{service.get('service_name', '')}"
    )

    print(
        f"Category    : "
        f"{service.get('category', '')}"
    )

    print(
        f"Description : "
        f"{service.get('description', '')}"
    )

    print(
        f"Status      : "
        f"{service.get('status', '')}"
    )


def search_services():
    """Search services by name or category."""

    services = load_services()

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
        for service in services
        if keyword in service.get(
            "service_name",
            ""
        ).lower()
        or keyword in service.get(
            "category",
            ""
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
        print_service(service)


def filter_services_by_status():
    """Filter services by Active or Inactive status."""

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
        print(
            "Invalid status selection."
        )
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
    """Update an existing service."""

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
        f"New name [{service.get('service_name', '')}]: "
    ).strip()

    new_category = input(
        f"New category [{service.get('category', '')}]: "
    ).strip()

    new_description = input(
        f"New description [{service.get('description', '')}]: "
    ).strip()

    print("\nStatus:")
    print("1. Active")
    print("2. Inactive")
    print("3. Keep current status")

    status_choice = input(
        "Select status: "
    ).strip()

    if status_choice not in [
        "",
        "1",
        "2",
        "3"
    ]:
        print(
            "Invalid status selection."
        )
        return

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

    if not save_services(services):
        print("Could not save changes.")
        return

    print(
        "Service updated successfully."
    )


def delete_service():
    """Delete an existing service."""

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
        "Are you sure you want to delete "
        "this service? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print(
            "Delete operation cancelled."
        )
        return

    services.remove(service)

    if not save_services(services):
        print("Could not save changes.")
        return

    print(
        f"Service {service_id} "
        f"deleted successfully."
    )


def service_menu():
    """Display the Service Management menu."""

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