"""
main.py

Entry point for the Veda Technology Business & Service Management System.

This is Day 1 of a 4-day major project for the Veda Technology
Python Programming Internship.

Day 1 focuses on a simple, beginner-friendly foundation:
- Program Management
- Service Management
- Customer / Inquiry Management
- Search and Filtering
- Basic CRUD with JSON storage
"""

import programs
import services
import inquiries
import search


def print_welcome():
    print("=" * 40)
    print("Veda Technology Business & Service")
    print("Management System")
    print("=" * 40)


def print_main_menu():
    print("\n========================================")
    print("Main Menu")
    print("========================================")
    print("1. Program Management")
    print("2. Service Management")
    print("3. Customer / Inquiry Management")
    print("4. Search")
    print("5. Exit")


def main():
    print_welcome()

    while True:
        print_main_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            programs.program_menu()
        elif choice == "2":
            services.service_menu()
        elif choice == "3":
            inquiries.inquiry_menu()
        elif choice == "4":
            search.search_menu()
        elif choice == "5":
            print("\nThank you for using Veda Technology")
            print("Business & Service Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option (1-5).")


if __name__ == "__main__":
    main()
