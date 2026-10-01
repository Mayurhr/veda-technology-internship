import programs
import services
import inquiries
import search
import reports


def print_welcome():
    """Display the application welcome message."""

    print("=" * 40)
    print("Veda Technology Business & Service")
    print("Management System")
    print("=" * 40)


def print_main_menu():
    """Display the main application menu."""

    print("\n========================================")
    print("Main Menu")
    print("========================================")
    print("1. Program Management")
    print("2. Service Management")
    print("3. Customer / Inquiry Management")
    print("4. Search")
    print("5. Business Reports")
    print("6. Exit")


def main():
    """Run the main application."""

    print_welcome()

    while True:

        print_main_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            programs.program_menu()

        elif choice == "2":
            services.service_menu()

        elif choice == "3":
            inquiries.inquiry_menu()

        elif choice == "4":
            search.search_menu()

        elif choice == "5":
            reports.report_menu()

        elif choice == "6":
            print(
                "\nThank you for using "
                "Veda Technology"
            )

            print(
                "Business & Service Management "
                "System. Goodbye!"
            )

            break

        else:
            print(
                "Invalid choice. "
                "Please select a valid option (1-6)."
            )


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n\nInput closed. Exiting the application. Goodbye!")