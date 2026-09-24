# Student Result & Grade Management System

A beginner-friendly, command-line Python application to manage student records, marks, grades and class performance.

## 1. Project Description
The system stores student details (ID, name, subjects, marks) in memory, automatically calculates total, percentage and grade, and generates a class performance summary. It is built with plain Python functions, lists and dictionaries.

## 2. Objective
Apply Python fundamentals — variables, data types, conditions, loops, functions, lists and dictionaries — in a small, well-structured application.

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
├── student_management.py        # Application source code
├── test_student_management.py   # unittest test cases
├── sample_output.txt            # Sample program run
└── README.md
```

## 6. Data Structure
Students are stored in a dictionary keyed by Student ID:
```python
students = {
    "S101": {
        "id": "S101",
        "name": "Rahul",
        "subjects": ["Maths", "Science", "English", "History", "CS"],
        "marks": {"Maths": 80, "Science": 90, "English": 70, "History": 85, "CS": 95},
        "total": 420,
        "percentage": 84.0,
        "grade": "A",
    }
}
```

## 7. Application Workflow
1. Program shows the menu and waits for a choice.
2. The selected function runs (add, update, search, view, summary).
3. Input is validated; errors print a clear message and return to the menu.
4. The menu repeats until the user chooses **Exit**.

## 8. Menu Options
| Option | Action |
|--------|--------|
| 1 | Add Student |
| 2 | Update Student |
| 3 | Search Student |
| 4 | View Student |
| 5 | View All Students |
| 6 | Performance Summary |
| 7 | Exit |

## 9. Mark Validation
Marks must be numeric and between 0 and 100 (inclusive). Invalid input (letters, blanks, negative numbers, values above 100) is rejected with a message and the user is asked again, so invalid marks never enter a record. Other validation covers empty names, invalid or duplicate Student IDs, empty subject lists and invalid menu choices.

## 10. Grade Calculation
Each subject is out of 100; percentage = total ÷ number of subjects.

| Percentage | Grade |
|-----------|-------|
| 90 – 100 | A+ |
| 80 – 89.99 | A |
| 70 – 79.99 | B |
| 60 – 69.99 | C |
| 50 – 59.99 | D |
| Below 50 | F |

## 11. Search and Update
- **Search** by Student ID; a clear message is shown if the student is not found.
- **Update** the name and/or re-enter all marks. Total, percentage and grade are recalculated automatically.

## 12. Performance Summary
Shows ID, name, total, percentage and grade for every student, plus the number of students, highest percentage (with the topper's name) and average percentage.

## 13. Testing
`test_student_management.py` covers grade boundaries, total and percentage calculation, invalid marks, student ID validation, and student creation/search.
```
python -m unittest test_student_management.py
```

## 14. Installation
1. Install Python 3.8 or newer.
2. Clone or download this repository.
3. No packages need to be installed.

## 15. How to Run
```
cd Student-Result-Grade-Management-System
python student_management.py
```

## 16. Sample Output
See [sample_output.txt](sample_output.txt) for a full run. Excerpt:
```
Student added successfully.

Student ID: S101
Name: Rahul
Total: 420
Percentage: 84.00%
Grade: A
```

## 17. Concepts Learned
- Variables and data types
- Conditions and loops
- Functions and modular design
- Lists and dictionaries
- Input validation and error handling
- Writing unit tests with `unittest`
- Writing clear documentation

## 18. Future Improvements
These are **not implemented yet**:
- OOP using classes (e.g. a `Student` class)
- Database integration for permanent storage
- REST API
- Authentication
- Web interface

## 19. Conclusion
This project demonstrates core Python fundamentals through a clean, modular command-line application with validation and tests. Data is kept in memory only, so records are lost when the program exits.
