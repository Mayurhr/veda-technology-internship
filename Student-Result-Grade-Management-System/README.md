# Student Result & Grade Management System

A beginner-friendly, command-line Python application to manage student records, marks, grades and class performance.

> **Day 2 update:** This project was improved from the Day 1 implementation by introducing an object-oriented design (`Student` and `StudentManager` classes) while keeping every Day 1 feature working exactly as before. See [Section 7](#7-student-class--oop-design-day-2) for details.

## 1. Project Description
The system stores student details (ID, name, subjects, marks) in memory, automatically calculates total, percentage and grade, and generates a class performance summary. It is built with Python, using a small set of classes for the data model and plain functions for validation, calculation and the command-line interface.

## 2. Objective
Apply Python fundamentals — variables, data types, conditions, loops, functions, lists, dictionaries and basic object-oriented design — in a small, well-structured application.

## 3. Features
- Add, update, search and view student records
- View all students in a table
- Marks validation (numeric, 0–100)
- Automatic total, percentage and grade calculation
- Performance summary with class statistics
- Input validation so normal invalid input never crashes the program
- Unit tests using `unittest`

## 4. Technologies Used
- Python 3 (standard library only, no external dependencies)
- VS Code, Git, GitHub

## 5. Project Structure
```
Student-Result-Grade-Management-System/
├── student_management.py        # Application source code (Student/StudentManager classes + CLI)
├── test_student_management.py   # unittest test cases
├── sample_output.txt            # Sample program run
└── README.md
```

## 6. Data Structures
Each student is a `Student` object; the collection of students is held inside a `StudentManager` object (keyed internally by Student ID, the same way the Day 1 dictionary was keyed):

```python
student = Student("S101", "Rahul", {"Maths": 80, "Science": 90, "English": 70, "History": 85, "CS": 95})
student.total        # 420   (derived from marks)
student.percentage    # 84.0  (derived from marks)
student.grade         # "A"   (derived from percentage)

manager = StudentManager()
manager.add("S101", "Rahul", {...})
manager.get("S101")   # -> the Student object, or None
```

## 7. Student Class / OOP Design (Day 2)
Day 1 stored each student as a plain dictionary and kept `total`/`percentage`/`grade` as pre-computed values inside it. Day 2 replaces that with two small classes:

- **`Student`** — holds `id`, `name` and `marks`. `total`, `percentage` and `grade` are **properties**, computed on demand from `marks`, so they can never drift out of sync after an update. It exposes `update_name()`, `update_marks()` and `print_details()` (the per-student view used by Add/Update/Search/View).
- **`StudentManager`** — owns the collection of `Student` objects and provides `add()`, `get()`, `exists()`, `all()`, `print_table()` and `performance_stats()`. It is the OOP replacement for the old module-level `students` dictionary.

Design choices, kept deliberately simple per the internship guidelines:
- No inheritance was introduced — there is only one kind of student record, so a class hierarchy would add complexity without benefit.
- The standalone calculation/validation functions (`calculate_total`, `calculate_percentage`, `calculate_grade`, `validate_marks`, `validate_student_id`) were kept as plain functions rather than turned into methods or static methods, since they don't need any student state and are also reused directly by the tests.
- All CLI/menu functions (`add_student`, `update_student`, etc.) keep their Day 1 names and behaviour; internally they now call `manager`/`Student` methods instead of editing a dictionary directly.

## 8. Application Workflow
1. Program shows the menu and waits for a choice.
2. The selected function runs (add, update, search, view, summary), operating on the shared `manager` (a `StudentManager`).
3. Input is validated; errors print a clear message and return to the menu.
4. The menu repeats until the user chooses **Exit**.

## 9. Menu Options
| Option | Action |
|--------|--------|
| 1 | Add Student |
| 2 | Update Student |
| 3 | Search Student |
| 4 | View Student |
| 5 | View All Students |
| 6 | Performance Summary |
| 7 | Exit |

## 10. Mark Validation
Marks must be numeric and between 0 and 100 (inclusive). Invalid input (letters, blanks, negative numbers, values above 100) is rejected with a message and the user is asked again, so invalid marks never enter a record. Other validation covers empty names, invalid or duplicate Student IDs, empty subject lists and invalid menu choices.

## 11. Grade Calculation
Each subject is out of 100; percentage = total ÷ number of subjects. `Student.percentage` and `Student.grade` recompute automatically whenever marks change.

| Percentage | Grade |
|-----------|-------|
| 90 – 100 | A+ |
| 80 – 89.99 | A |
| 70 – 79.99 | B |
| 60 – 69.99 | C |
| 50 – 59.99 | D |
| Below 50 | F |

## 12. Search and Update
- **Search** by Student ID; a clear message is shown if the student is not found.
- **Update** the name and/or re-enter all marks via `student.update_name()` / `student.update_marks()`. Total, percentage and grade are recalculated automatically because they are derived properties.

## 13. Performance Summary
Shows ID, name, total, percentage and grade for every student, plus the number of students, highest percentage (with the topper's name) and average percentage, via `StudentManager.print_table()` and `StudentManager.performance_stats()`.

## 14. Unit Testing
`test_student_management.py` covers:
- Grade boundaries, total and percentage calculation (module-level functions)
- `Student` creation, total/percentage/grade derivation, name update, marks update (and recalculation), and that marks are copied (not shared) into the object
- `StudentManager` add/exists/get (found and missing), listing all students, performance stats, and updating a student through the manager
- CLI-level behaviour: search (found/missing), and that "no students yet" cases (performance summary, view all) don't raise errors

Run:
```
python -m unittest discover -v
```

## 15. Installation
1. Install Python 3.8 or newer.
2. Clone or download this repository.
3. No packages need to be installed.

## 16. How to Run
```
cd Student-Result-Grade-Management-System
python student_management.py
```

## 17. Sample Output
See [sample_output.txt](sample_output.txt) for a full run — the Day 2 OOP refactor is behavior-preserving, so this output is identical to Day 1. Excerpt:
```
Student added successfully.

Student ID: S101
Name: Rahul
Total: 420
Percentage: 84.00%
Grade: A
```

## 18. Concepts Learned
- Variables and data types
- Conditions and loops
- Functions and modular design
- Lists and dictionaries
- Object-oriented programming: classes, properties, encapsulating state and behaviour together
- Input validation and error handling
- Writing unit tests with `unittest`, including tests for a class-based design
- Writing clear documentation

## 19. Future Improvements
These are **not implemented yet**:
- Database integration for permanent storage
- REST API (building and consuming one, per internship feedback)
- Authentication
- Web interface
- More real-world practice projects applying these same OOP and testing patterns

## 20. Conclusion
This project demonstrates core Python fundamentals through a clean, modular command-line application with validation and tests. Day 2 improved on Day 1 by introducing a small, focused object-oriented design (`Student`, `StudentManager`) without over-engineering it — no inheritance was added since none was needed — while preserving 100% of the original functionality and output. Data is kept in memory only, so records are lost when the program exits.
