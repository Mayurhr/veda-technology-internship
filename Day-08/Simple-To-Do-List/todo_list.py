tasks = []
def add_task():
    task = input("Enter a task: ")
    tasks.append(task)
    print("Task added successfully!")

def view_tasks():
    if len(tasks) == 0:
        print("No tasks available.")
    else:
        print("\nTo-Do List:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task}")


def update_task():
    view_tasks()

    if len(tasks) == 0:
        return

    number = int(input("Enter task number to update: "))

    if 1 <= number <= len(tasks):
        new_task = input("Enter new task: ")
        tasks[number - 1] = new_task
        print("Task updated successfully!")
    else:
        print("Invalid task number.")


def remove_task():
    view_tasks()

    if len(tasks) == 0:
        return

    number = int(input("Enter task number to remove: "))

    if 1 <= number <= len(tasks):
        tasks.pop(number - 1)
        print("Task removed successfully!")
    else:
        print("Invalid task number.")


while True:
    print("\n--- To-Do List ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Remove Task")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        update_task()
    elif choice == "4":
        remove_task()
    elif choice == "5":
        print("Thank you for using the To-Do List!")
        break
    else:
        print("Invalid choice. Please try again.")
