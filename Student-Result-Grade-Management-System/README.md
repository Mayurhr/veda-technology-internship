# Student Result & Grade Management System

A command-line Python application to manage student details, subjects, marks, grades and academic performance — built as a three-day Python Programming Internship project (Veda Technology).

## 1. Project Overview
This is the **final, submission-ready version** of the project. It was built progressively over three internship days on the same codebase:

- **Day 1** established the core functionality: add/update/search/view students, mark validation, total/percentage/grade calculation, a menu-driven CLI, an initial `unittest` suite and README.
- **Day 2** introduced object-oriented design — a `Student` class and a `StudentManager` class — replacing the plain dictionary model, and restructured the tests around it, without changing any menu behaviour or output.
- **Day 3 (this version)** is a final polish pass: stronger validation guarantees at the class level, a few more edge-case tests, a graceful exit on Ctrl+C/Ctrl+D instead of a crash, and finished documentation. No new features, menu options or grading rules were added.

## 2. Description
The system stores student details (ID, name, subjects, marks) in memory, automatically calculates total, percentage and grade, and generates a class performance summary, all through a simple text menu.

## 3. Objective
Apply Python fundamentals — variables, data types, conditions, loops, functions, lists, dictionaries — together with basic object-oriented application design, input validation and unit testing.

## 4. Features
- Add, update, search and view student records
- View all students in a table
- Marks validation (numeric, 0–100)
- Student ID validation (letters/digits only) and duplicate-ID rejection
- Subject list validation (at least one subject, no duplicate subject names)
- Automatic total, percentage and grade calculation
- Performance summary with class statistics (count, highest, average)
- Input validation throughout, so normal invalid input never crashes the program
- Graceful exit on Ctrl+C / Ctrl+D
- Unit tests using `unittest` (33 tests)

## 5. Technologies Used
- Python 3 (standard library only — no external dependencies)
- `unittest` and `unittest.mock` for testing
- VS Code, Git, GitHub

## 6. Project Structure
```
Student-Result-Grade-Management-System/
├── student_management.py        # Application source code (Student/StudentManager classes + CLI)
├── test_student_management.py   # unittest test suite (33 tests)
├── README.md                    # This file
└── sample_output.txt            # Sample end-to-end program run
```
No new files were added on Day 3 — the original four-file structure from Day 1/2 was kept as-is, since nothing about this project's size needs more than that.

## 7. Student Class
`Student` holds one student's `id`, `name` and `marks` (a `{subject: mark}` dict). `total`, `percentage`, `subjects` and `grade` are **properties**, computed on demand from `marks`, so they can never go out of sync after an update.

| Member | Description |
|---|---|
| `subjects` | List of subject names (property) |
| `total` | Sum of all marks (property) |
| `percentage` | `total` ÷ number of subjects (property) |
| `grade` | Grade letter derived from `percentage` (property) |
| `update_name(name)` | Replace the student's name |
| `update_marks(marks)` | Replace all marks (total/percentage/grade recalculate automatically) |
| `summary_row()` | `(id, name, total, percentage, grade)` tuple, used by table rows |
| `print_details()` | Prints the full per-student view used by Add/Update/Search/View |

No inheritance was introduced: there is only one kind of academic record in this project, so a class hierarchy would add complexity without a real benefit. That matches the internship feedback's own guidance to add OOP only where it naturally fits.

## 8. StudentManager Class
`StudentManager` owns the collection of `Student` objects (keyed internally by Student ID, replacing the Day 1 dictionary) and is the single source of truth the CLI operates on:

| Member | Description |
|---|---|
| `add(id, name, marks)` | Create and store a new student. **Day 3:** raises `ValueError` on a duplicate ID, so the manager protects its own data even if called outside the CLI's own duplicate check. |
| `get(id)` | Return the `Student`, or `None` (with a "not found" message) |
| `exists(id)` | `True`/`False` — used by the CLI to give a friendly message before asking for a name |
| `all()` | List of every `Student` |
| `clear()` | Remove all students (used by the tests) |
| `print_table()` | Prints the ID/Name/Total/Percentage/Grade table |
| `performance_stats()` | Returns `(topper, highest_percentage, average_percentage)`. **Day 3:** raises `ValueError` on an empty class instead of crashing with a confusing `ZeroDivisionError`/`ValueError` from `max()`/`sum()`. |

## 9. Grade Calculation
Each subject is out of 100; percentage = total ÷ number of subjects. This grading behaviour is unchanged from Day 1/2 — no bug was found in it.

| Percentage | Grade |
|-----------|-------|
| 90 – 100 | A+ |
| 80 – 89.99 | A |
| 70 – 79.99 | B |
| 60 – 69.99 | C |
| 50 – 59.99 | D |
| Below 50 | F |

## 10. Input Validation
| Input | Rule |
|---|---|
| Student name | Rejected if empty/blank |
| Student ID | Rejected unless non-empty letters/digits (e.g. `S101`) |
| Duplicate Student ID | Rejected — both at the CLI (before asking for a name) and inside `StudentManager.add()` |
| Subject list | Rejected if empty, or if it contains duplicate subject names (case-insensitive) |
| Marks | Rejected unless numeric and between 0 and 100 inclusive (0 and 100 themselves are valid) |
| Menu choice | Anything outside 1–7 shows "Invalid choice" and redisplays the menu |
| Empty student database | View All / Performance Summary show a message instead of erroring |
| Search for a missing ID | Shows a "not found" message instead of erroring |
| Ctrl+C / Ctrl+D at any prompt | Caught in `main()`; prints "Interrupted. Goodbye!" and exits cleanly |

## 11. Search and Update
- **Search** by Student ID; a clear message is shown if the student is not found.
- **Update** the name and/or re-enter all marks via `student.update_name()` / `student.update_marks()`. Total, percentage and grade recalculate automatically because they are derived properties.

## 12. Performance Summary
Shows ID, name, total, percentage and grade for every student, plus the number of students, the highest percentage (with the topper's name) and the average percentage, via `StudentManager.print_table()` and `StudentManager.performance_stats()`.

## 13. Unit Testing
`test_student_management.py` contains **33 tests**, organised by what they cover:

- `TestCalculations` — total, percentage, and all grade boundaries
- `TestValidation` — valid/invalid marks, Student ID format
- `TestStudentClass` — creation, derived properties, name/marks updates and recalculation, marks isolation (copy, not shared reference)
- `TestStudentManager` — add/exists/get (found & missing), listing all students, performance stats, updating through the manager, **duplicate-ID rejection**, **performance stats on an empty manager**
- `TestCLIActions` — search (found/missing), empty-database safety for view-all and performance summary, **duplicate ID / empty name / invalid ID rejected at the CLI**
- `TestInputValidationLoops` — mark boundaries (0 and 100 accepted), out-of-range/non-numeric marks re-prompted, empty subject list re-prompted, duplicate subjects re-prompted
- `TestMainGracefulExit` — Ctrl+C (`KeyboardInterrupt`) and Ctrl+D (`EOFError`) are caught by `main()`, not left to crash the program

Run:
```
python -m unittest discover -v
```

## 14. How to Install
1. Install Python 3.8 or newer.
2. Clone or download this repository.
3. No packages need to be installed — standard library only.

## 15. How to Run
```
cd Student-Result-Grade-Management-System
python student_management.py
```

## 16. Sample Output
See [sample_output.txt](sample_output.txt) for a full, realistic run covering: starting the app, adding a student (with an invalid-marks retry), a rejected duplicate ID, an invalid menu choice, searching an existing and a missing student, updating a student, viewing a single student, viewing all students, the performance summary, and a safe exit.

## 17. Testing Results
```
$ python -m unittest discover -v
...
----------------------------------------------------------------------
Ran 33 tests in 0.004s

OK
```
All 33 tests pass. `python -m py_compile student_management.py` reports no syntax errors. The full menu workflow (add → invalid marks → duplicate ID → search hit/miss → update → view all → performance summary → exit, plus a Ctrl+C mid-menu) was run manually end-to-end with no crashes.

## 18. Concepts Learned
- Variables, data types, conditions and loops
- Functions and modular design
- Lists and dictionaries
- Object-oriented programming: classes, properties, encapsulating state and behaviour together, and knowing when *not* to use inheritance
- Input validation and defensive programming (validating at more than one layer — CLI and manager)
- Handling runtime exceptions (`KeyboardInterrupt`, `EOFError`) for a robust CLI
- Writing unit tests with `unittest`, including `unittest.mock.patch` to test interactive `input()`-driven code
- Writing clear, GitHub-ready documentation

## 19. Future Improvements
Deliberately **not implemented**, to keep this a focused Python-fundamentals/OOP project as scoped:
- Database integration for permanent storage (records are in-memory only and lost on exit)
- A REST API (building and consuming one, per internship feedback, is left for a dedicated project)
- Authentication
- A web or GUI interface
- More real-world practice projects applying these same OOP and testing patterns, as suggested in the internship feedback

## 20. Conclusion
Across three days, this project grew from a working functional CLI (Day 1) into a small, genuinely object-oriented application (Day 2) and finally into a polished, well-tested, defensively-validated piece of software (Day 3) — without ever over-engineering it: no inheritance, no frameworks, no external dependencies, just a `Student` and a `StudentManager` doing one job well. Every Day 1 and Day 2 feature and output still works exactly as before; Day 3 only added robustness (duplicate/empty-state guards, graceful interrupt handling) and finished the test suite and documentation for submission.

## 21. Repository Note
This project was developed and finalized locally / in a sandboxed environment. If you're pushing this to GitHub yourself, from inside `Student-Result-Grade-Management-System/`:
```
git add student_management.py test_student_management.py README.md sample_output.txt
git commit -m "Complete Student Result Grade Management System"
git push
```
