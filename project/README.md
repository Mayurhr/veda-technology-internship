# Veda Technology Business & Service Management System

**Veda Technology Python Programming Internship — Major Project — Day 1 of 4**

## Description

A Python-based command-line application that represents the core operations
of a technology and digital-services organization: managing training
programs, digital services, and customer inquiries. This is **Day 1** of a
4-day major project. It builds a clean, extensible foundation that Days 2–4
will continue to build on without needing to rewrite existing code.

## Objective

Apply core Python programming concepts — functions, dictionaries, lists,
file handling, input validation, and basic reporting — to a realistic
technology-business scenario.

## Tools Used

- Python 3 (standard library only)
- VS Code
- JSON for data storage
- Git / GitHub

## Features (Implemented on Day 1)

- Program Management (Add / View / Search / Update / Delete)
- Service Management (Add / View / Search / Update / Delete)
- Customer / Inquiry Management (Add / View / Search / Update Status)
- Combined Search menu across all three record types
- Filter any record type by status
- JSON-based persistent storage, auto-created on first run
- Input validation (required fields, basic email check, unique IDs)
- Missing-record handling with clear messages
- Beginner-friendly, menu-driven CLI
- Unit tests for the core data-management functions

## Project Structure

```
veda_day1/
├── main.py            # CLI entry point and main menu
├── programs.py         # Program Management (CRUD + search)
├── services.py          # Service Management (CRUD + search)
├── inquiries.py          # Customer / Inquiry Management
├── search.py               # Combined search / status filter menu
├── storage.py                # JSON load/save + ID generation helpers
├── validation.py               # Reusable input validation helpers
├── test_core.py                  # Unit tests for core functions
├── sample_output.txt              # Recorded sample run of the program
├── README.md                        # This file
└── data/                              # Created automatically on first run
    ├── programs.json
    ├── services.json
    └── inquiries.json
```

## Program Management

Each program has: `program_id`, `program_name`, `category`, `duration`,
`status`. Supports adding, listing, searching by name, updating (blank
input keeps the existing value), and deleting.

## Service Management

Each service has: `service_id`, `service_name`, `category`, `description`,
`status`. Supports the same CRUD and search operations as programs,
searchable by category.

## Customer / Inquiry Management

Each inquiry has: `inquiry_id`, `customer_name`, `email`, `service`,
`message`, `status`. New inquiries start as `Open`. Supports adding,
listing, searching by customer name, and updating status.

## CRUD Operations

All three modules implement Create, Read, Update, and Delete (inquiries
currently expose status updates rather than full record edits, matching
Day 1's scope) through small, reusable functions shared via `storage.py`
and `validation.py`.

## Search and Filtering

The **Search** menu (option 4 on the main menu) lets you:
- Search programs by name
- Search services by category
- Search inquiries by customer name
- Filter any of the three record types by status

## Data Storage

Data is stored as JSON files inside the `data/` folder, one file per
record type. On first run, the folder and files are created automatically
with a small set of sample records. On every later run, existing data is
loaded from these files, so re-running the program does **not** recreate
or duplicate the sample records.

## Validation

- Required text fields cannot be submitted empty (the program re-prompts).
- Email addresses go through a basic check for an `@` and a `.` in the
  domain part.
- Record IDs are generated automatically and are always unique.
- Updating or deleting a record with an ID that doesn't exist shows a
  clear "not found" message instead of crashing.
- Invalid menu choices are caught and re-prompted instead of raising
  errors.

## How to Run

```bash
cd veda_day1
python main.py
```

No external dependencies are required — only the Python standard library.

To run the unit tests:

```bash
python -m unittest test_core.py -v
```

## Sample Output

See [`sample_output.txt`](sample_output.txt) for a full recorded terminal
session covering: startup, adding and viewing a program, adding and
viewing a service, adding and viewing an inquiry, searching each record
type, updating a program, and handling a nonexistent record ID.

## Concepts Learned

- Structuring a multi-file Python project with reusable modules
- Reading and writing JSON files for persistent storage
- Writing reusable, beginner-friendly validation functions
- Designing a menu-driven CLI with clear submenus
- Handling missing/invalid records and user input gracefully
- Writing basic `unittest` test cases for core logic

## Future Enhancements (Planned for Days 2–4)

- Full CRUD (including edit) for inquiries
- Reporting/summary features (e.g. counts by status or category)
- More advanced filtering and sorting options
- Possibly moving from a flat JSON store to a lightweight database
- Additional automated tests covering menu flows

## Conclusion

Day 1 delivers a working, tested foundation for the Veda Technology
Business & Service Management System: program, service, and inquiry
management with JSON persistence, validation, and a simple CLI — built to
be extended, not rewritten, over the remaining three days.
