"""Student Result & Grade Management System.

A simple command-line application to manage student records, marks,
grades and a class performance summary.

Grading system (based on percentage):
    90 - 100 : A+
    80 - 89  : A
    70 - 79  : B
    60 - 69  : C
    50 - 59  : D
    Below 50 : F
"""

students = {}


# ---------- Calculation functions ----------

def calculate_total(marks):
    """Return the sum of all marks in a dictionary {subject: mark}."""
    return sum(marks.values())


def calculate_percentage(marks):
    """Return the percentage, assuming each subject is out of 100."""
    if not marks:
        return 0.0
    return calculate_total(marks) / len(marks)


def calculate_grade(percentage):
    """Return the grade letter for a given percentage."""
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    return "F"


# ---------- Validation functions ----------

def validate_marks(value):
    """Return the mark as a float if valid (0-100), otherwise None."""
    try:
        mark = float(value)
    except (TypeError, ValueError):
        return None
    if mark != mark or mark < 0 or mark > 100:  # mark != mark catches NaN
        return None
    return mark


def validate_student_id(student_id):
    """A valid ID is a non-empty string of letters/digits (e.g. S101)."""
    return bool(student_id) and student_id.isalnum()


def format_number(value):
    """Show whole numbers without the trailing .0 (420.0 -> 420)."""
    return str(int(value)) if value == int(value) else str(value)


# ---------- Input helpers ----------

def read_marks(subject_names):
    """Ask for a mark for each subject until a valid one is entered."""
    marks = {}
    for subject in subject_names:
        while True:
            mark = validate_marks(input(f"Enter marks for {subject} (0-100): ").strip())
            if mark is None:
                print("Invalid marks. Enter a number between 0 and 100.")
                continue
            marks[subject] = mark
            break
    return marks


def read_subjects():
    """Ask for a comma-separated list of subjects."""
    while True:
        raw = input("Enter subjects (comma separated): ")
        names = [s.strip() for s in raw.split(",") if s.strip()]
        if not names:
            print("Enter at least one subject.")
        elif len(set(n.lower() for n in names)) != len(names):
            print("Subjects must be unique.")
        else:
            return names


# ---------- Student operations ----------

def build_student(student_id, name, marks):
    """Create a student record with total, percentage and grade calculated."""
    percentage = calculate_percentage(marks)
    return {
        "id": student_id,
        "name": name,
        "subjects": list(marks.keys()),
        "marks": marks,
        "total": calculate_total(marks),
        "percentage": percentage,
        "grade": calculate_grade(percentage),
    }


def add_student():
    student_id = input("Enter Student ID: ").strip().upper()
    if not validate_student_id(student_id):
        print("Invalid Student ID. Use letters and digits only (e.g. S101).")
        return
    if student_id in students:
        print(f"Student ID {student_id} already exists.")
        return

    name = input("Enter Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    marks = read_marks(read_subjects())
    students[student_id] = build_student(student_id, name, marks)
    print("\nStudent added successfully.")
    view_student(student_id)


def update_student():
    student_id = input("Enter Student ID to update: ").strip().upper()
    student = search_student(student_id)
    if student is None:
        return

    new_name = input(f"New name [{student['name']}] (Enter to keep): ").strip()
    if new_name:
        student["name"] = new_name

    choice = input("Update marks? (y/n): ").strip().lower()
    if choice == "y":
        marks = read_marks(read_subjects())
        student.update(build_student(student_id, student["name"], marks))
    print("\nStudent updated successfully.")
    view_student(student_id)


def search_student(student_id):
    """Return the student record, or None (with a message) if not found."""
    student = students.get(student_id)
    if student is None:
        print(f"Student with ID {student_id or '(empty)'} not found.")
    return student


def view_student(student_id):
    student = students.get(student_id)
    if student is None:
        print(f"Student with ID {student_id} not found.")
        return
    print(f"\nStudent ID: {student['id']}")
    print(f"Name: {student['name']}")
    for subject, mark in student["marks"].items():
        print(f"  {subject}: {format_number(mark)}")
    print(f"Total: {format_number(student['total'])}")
    print(f"Percentage: {student['percentage']:.2f}%")
    print(f"Grade: {student['grade']}")


def view_all_students():
    if not students:
        print("No students found.")
        return
    print(f"\n{'ID':<8}{'Name':<15}{'Total':<10}{'Percentage':<12}{'Grade'}")
    print("-" * 50)
    for s in students.values():
        print(f"{s['id']:<8}{s['name']:<15}{format_number(s['total']):<10}"
              f"{s['percentage']:<12.2f}{s['grade']}")


def performance_summary():
    if not students:
        print("No students found. Add students first.")
        return
    print("\n===== PERFORMANCE SUMMARY =====")
    print(f"{'ID':<8}{'Name':<15}{'Total':<10}{'Percentage':<12}{'Grade'}")
    print("-" * 50)
    for s in students.values():
        print(f"{s['id']:<8}{s['name']:<15}{format_number(s['total']):<10}"
              f"{s['percentage']:<12.2f}{s['grade']}")

    percentages = [s["percentage"] for s in students.values()]
    topper = max(students.values(), key=lambda s: s["percentage"])
    print("-" * 50)
    print(f"Number of students: {len(students)}")
    print(f"Highest percentage: {max(percentages):.2f}% ({topper['name']})")
    print(f"Average percentage: {sum(percentages) / len(percentages):.2f}%")


# ---------- Menu ----------

def show_menu():
    print("\n===== STUDENT RESULT & GRADE MANAGEMENT SYSTEM =====\n")
    print("1. Add Student")
    print("2. Update Student")
    print("3. Search Student")
    print("4. View Student")
    print("5. View All Students")
    print("6. Performance Summary")
    print("7. Exit")


def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            update_student()
        elif choice == "3":
            student_id = input("Enter Student ID to search: ").strip().upper()
            if search_student(student_id):
                print("Student found.")
                view_student(student_id)
        elif choice == "4":
            view_student(input("Enter Student ID: ").strip().upper())
        elif choice == "5":
            view_all_students()
        elif choice == "6":
            performance_summary()
        elif choice == "7":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
