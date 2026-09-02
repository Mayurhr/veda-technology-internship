contacts = {}

while True:
    print("\n--- Contact Book ---")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. View Contacts")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter name: ")
        phone = input("Enter phone number: ")

        if name in contacts:
            print("Contact already exists.")
        else:
            contacts[name] = phone
            print("Contact added successfully.")

    elif choice == "2":
        name = input("Enter name to search: ")

        if name in contacts:
            print("Phone:", contacts[name])
        else:
            print("Contact not found.")

    elif choice == "3":
        name = input("Enter name to update: ")

        if name in contacts:
            phone = input("Enter new phone number: ")
            contacts[name] = phone
            print("Contact updated successfully.")
        else:
            print("Contact not found.")

    elif choice == "4":
        name = input("Enter name to delete: ")

        if name in contacts:
            del contacts[name]
            print("Contact deleted successfully.")
        else:
            print("Contact not found.")

    elif choice == "5":
        if contacts:
            print("\nContacts:")
            for name, phone in contacts.items():
                print(name, ":", phone)
        else:
            print("No contacts available.")

    elif choice == "6":
        print("Thank you for using Contact Book.")
        break

    else:
        print("Invalid choice. Please try again.")
