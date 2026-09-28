"""
search.py

Provides a combined Search menu that lets the user search
programs, services, and inquiries, or filter any of them by status.
"""

import programs
import services
import inquiries


def filter_by_status():
    print("\n--- Filter Records by Status ---")
    print("1. Programs")
    print("2. Services")
    print("3. Inquiries")
    choice = input("Choose what to filter (1-3): ").strip()

    status = input("Enter status to filter by: ").strip().lower()

    if choice == "1":
        records = programs.load_programs()
        results = [r for r in records if r["status"].lower() == status]
        for r in results:
            programs.print_program(r)
    elif choice == "2":
        records = services.load_services()
        results = [r for r in records if r["status"].lower() == status]
        for r in results:
            services.print_service(r)
    elif choice == "3":
        records = inquiries.load_inquiries()
        results = [r for r in records if r["status"].lower() == status]
        for r in results:
            inquiries.print_inquiry(r)
    else:
        print("Invalid choice.")
        return

    if choice in ("1", "2", "3") and not results:
        print("No records found with that status.")


def search_menu():
    while True:
        print("\n========================================")
        print("Search")
        print("========================================")
        print("1. Search Programs by Name")
        print("2. Search Services by Category")
        print("3. Search Inquiries by Customer Name")
        print("4. Filter Records by Status")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            programs.search_programs()
        elif choice == "2":
            services.search_services()
        elif choice == "3":
            inquiries.search_inquiries()
        elif choice == "4":
            filter_by_status()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please select a valid option (1-5).")
