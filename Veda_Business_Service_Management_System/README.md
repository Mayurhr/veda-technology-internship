# Veda Technology Business & Service Management System

A simple, modular, menu-driven Python console application for managing programs, digital services,
customer inquiries, search/filtering and basic business reports. Data is stored in JSON files.
Built as part of the Veda Technology Python Programming Internship. Only synthetic sample data is used.

## Objectives

- Practise functions, modules, dictionaries, lists, loops and menus in Python
- Implement full CRUD (create, read, update, delete) with input validation
- Persist data with JSON file handling and exception handling
- Provide search, status filtering and summary reports
- Write unit tests with `unittest`

## Features

- **Programs** (`PRG001`, `PRG002`, ...): add, view, search, filter by status (Active/Inactive), update, delete
- **Services** (`SVC001`, ...): add, view, search, filter by status (Active/Inactive), update, delete
- **Inquiries** (`INQ001`, ...): add, view, search, filter by status (Open / In Progress / Closed), update, update status only, delete
- **Search**: programs/services by name or category; inquiries by customer name, email or service (case-insensitive, partial match); status filter for all three record types
- **Reports**: total programs/services/inquiries, status counts, programs by category, services by category, inquiries by status
- **Validation**: empty input is rejected and re-asked, email format check, status check, case-insensitive IDs, missing/invalid IDs give a message, invalid menu choices are handled
- **Safe storage**: missing JSON files are created, corrupted JSON does not crash the app (the bad file is kept as `<name>.json.corrupt` instead of being overwritten), saves are written to a temp file first

## Technologies Used

Python 3 (standard library only: `json`, `os`, `unittest`). No external dependencies.

## Project Structure

```text
Veda_Technology_Business_Service_Management_System/
├── main.py            # main menu
├── programs.py        # program CRUD, search, filter
├── services.py        # service CRUD, search, filter
├── inquiries.py       # inquiry CRUD, status update, search, filter
├── search.py          # combined search and filter menu
├── reports.py         # business reports
├── storage.py         # JSON load/save and ID generation
├── validation.py      # input and email/ID/status validation
├── test_core.py       # unit tests
├── README.md
├── FINAL_TEST_REPORT.md
├── sample_output.txt
└── data/
    ├── programs.json
    ├── services.json
    └── inquiries.json
```

## How to Run

```bash
python main.py
```

Developed and tested on Python 3.12 (standard library only). The `data/` folder is located next to the code,
so the program works from any working directory.

## How to Run Tests

```bash
python -m unittest discover -v
# or
python -m unittest test_core -v
```

The tests use a temporary data folder, so your real JSON files are never modified.

## JSON Storage

Records are lists of dictionaries in `data/programs.json`, `data/services.json`, `data/inquiries.json`.

| File | Fields |
|------|--------|
| programs.json | program_id, program_name, category, duration, status |
| services.json | service_id, service_name, category, description, status |
| inquiries.json | inquiry_id, customer_name, email, service, message, status |

New IDs are `max existing number + 1`, so IDs stay unique and are not reused after a delete.
If a file is missing it is created (programs and services get their default sample records, inquiries get one sample record).

## Module Descriptions

- `main.py` - welcome message and main menu loop; exits cleanly on Ctrl+C / closed input
- `programs.py`, `services.py`, `inquiries.py` - one module per record type with its menu
- `search.py` - search and filter menu across all record types
- `reports.py` - counts and category/status reports computed from the JSON data
- `storage.py` - `load_data`, `save_data`, `generate_next_id`
- `validation.py` - `is_not_empty`, `is_valid_email`, `find_record_by_id`, `id_exists`, `is_valid_status` and input helpers

## Sample Functionality

See `sample_output.txt` for a real captured run. Example: choose `1` (Program Management) -> `1` (Add Program),
enter name, category, duration, and status; the program gets the next ID (e.g. `PRG004`) and is saved to JSON.

## Testing Information

`test_core.py` contains 70 unit tests covering storage (missing/empty/corrupt files), ID generation, validation,
and every Program, Service and Inquiry operation (including invalid input and missing IDs), search, filtering,
reports and the main menu. Results are in `FINAL_TEST_REPORT.md`.

Known limitations: the interactive menus are tested by simulating keyboard input, not with a GUI; the email check is a basic
format check (needs `@` and a dot in the domain); there is no authentication; deleting a service does not change inquiries that mention it
(inquiries store the service as free text).

## Future Enhancements

- Link inquiries to service IDs
- Export reports to CSV
- Date/time stamps on inquiries
- Optional database (SQLite) storage
- Simple GUI or web interface

## Conclusion

The project is a working, modular console application that demonstrates CRUD, validation, searching, reporting and
JSON persistence using only the Python standard library.
