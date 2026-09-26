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


# ---------- Student (OOP model) ----------

class Student:
    """A single student's record.

    Holds the student's id, name and marks, and derives total,
    percentage and grade from the marks whenever they are needed, so
    those values can never go out of sync with the marks.
    """

    def __init__(self, student_id, name, marks):
        self.id = student_id
        self.name = name
        self.marks = dict(marks)

    # --- derived (read-only) properties ---

    @property
    def subjects(self):
        return list(self.marks.keys())

    @property
    def total(self):
        return calculate_total(self.marks)

    @property
    def percentage(self):
        return calculate_percentage(self.marks)

    @property
    def grade(self):
        return calculate_grade(self.percentage)

    # --- behaviour ---

    def update_name(self, name):
        """Replace the student's name (caller validates it's non-empty)."""
        self.name = name

    def update_marks(self, marks):
        """Replace all marks; total/percentage/grade recalculate automatically."""
        self.marks = dict(marks)

    def summary_row(self):
        """Return the (id, name, total, percentage, grade) tuple used in tables."""
        return (self.id, self.name, self.total, self.percentage, self.grade)

    def print_details(self):
        """Print the full per-student view used by Add/Update/Search/View."""
        print(f"\nStudent ID: {self.id}")
        print(f"Name: {self.name}")
        for subject, mark in self.marks.items():
            print(f"  {subject}: {format_number(mark)}")
        print(f"Total: {format_number(self.total)}")
        print(f"Percentage: {self.percentage:.2f}%")
        print(f"Grade: {self.grade}")


class StudentManager:
    """Owns the collection of students and the operations on it.

    This is the OOP replacement for the old module-level ``students``
    dictionary: it stores ``Student`` objects keyed by student ID and
    exposes the same set of operations the CLI needs (add, update,
    search, view, view all, performance summary).
    """

    def __init__(self):
        self._students = {}

    def __len__(self):
        return len(self._students)

    def exists(self, student_id):
        return student_id in self._students

    def add(self, student_id, name, marks):
        """Create and store a new Student. Raises ValueError on a duplicate ID.

        The CLI already checks ``exists()`` before calling this (so it can
        show a friendly message without asking for name/marks first), but
        ``add`` also refuses duplicates itself so the manager can never end
        up in an inconsistent state if it's ever called another way (e.g.
        directly, or from a test).
        """
        if student_id in self._students:
            raise ValueError(f"Student ID {student_id} already exists.")
        student = Student(student_id, name, marks)
        self._students[student_id] = student
        return student

    def get(self, student_id):
        """Return the Student, or None (printing a message) if not found."""
        student = self._students.get(student_id)
        if student is None:
            print(f"Student with ID {student_id or '(empty)'} not found.")
        return student

    def all(self):
        return list(self._students.values())

    def clear(self):
        self._students.clear()

    def print_table(self, students=None):
        rows = self.all() if students is None else students
        print(f"{'ID':<8}{'Name':<15}{'Total':<10}{'Percentage':<12}{'Grade'}")
        print("-" * 50)
        for s in rows:
            print(f"{s.id:<8}{s.name:<15}{format_number(s.total):<10}"
                  f"{s.percentage:<12.2f}{s.grade}")

    def performance_stats(self):
        """Return (topper, highest_percentage, average_percentage).

        Raises ValueError if there are no students yet, since "highest" and
        "average" are meaningless for an empty class. The CLI's
        ``performance_summary()`` already checks ``len(manager)`` before
        calling this, so callers see the friendly CLI message rather than
        this exception during normal use.
        """
        if not self._students:
            raise ValueError("performance_stats() requires at least one student.")
        percentages = [s.percentage for s in self._students.values()]
        topper = max(self._students.values(), key=lambda s: s.percentage)
        return topper, max(percentages), sum(percentages) / len(percentages)


# Single shared manager used by the CLI (equivalent to the old
# module-level `students` dictionary from the Day 1 version).
manager = StudentManager()


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


# ---------- Student operations (CLI actions) ----------

def add_student():
    student_id = input("Enter Student ID: ").strip().upper()
    if not validate_student_id(student_id):
        print("Invalid Student ID. Use letters and digits only (e.g. S101).")
        return
    if manager.exists(student_id):
        print(f"Student ID {student_id} already exists.")
        return

    name = input("Enter Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    marks = read_marks(read_subjects())
    manager.add(student_id, name, marks)
    print("\nStudent added successfully.")
    view_student(student_id)


def update_student():
    student_id = input("Enter Student ID to update: ").strip().upper()
    student = manager.get(student_id)
    if student is None:
        return

    new_name = input(f"New name [{student.name}] (Enter to keep): ").strip()
    if new_name:
        student.update_name(new_name)

    choice = input("Update marks? (y/n): ").strip().lower()
    if choice == "y":
        marks = read_marks(read_subjects())
        student.update_marks(marks)
    print("\nStudent updated successfully.")
    view_student(student_id)


def search_student(student_id):
    """Return the Student, or None (with a message) if not found."""
    return manager.get(student_id)


def view_student(student_id):
    student = manager.get(student_id)
    if student is None:
        return
    student.print_details()


def view_all_students():
    if len(manager) == 0:
        print("No students found.")
        return
    print()
    manager.print_table()


def performance_summary():
    if len(manager) == 0:
        print("No students found. Add students first.")
        return
    print("\n===== PERFORMANCE SUMMARY =====")
    manager.print_table()

    topper, highest, average = manager.performance_stats()
    print("-" * 50)
    print(f"Number of students: {len(manager)}")
    print(f"Highest percentage: {highest:.2f}% ({topper.name})")
    print(f"Average percentage: {average:.2f}%")


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
    try:
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
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D during any input() call: exit cleanly instead of
        # showing a traceback.
        print("\n\nInterrupted. Goodbye!")


if __name__ == "__main__":
    main()
