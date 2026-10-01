# Final Test Report

- **Test date:** 2026-10-01
- **Python version:** 3.12.3
- **Test environment:** Linux; standard library only (pytest is not installed or configured, so it was not run)

## Application startup
`python main.py` starts successfully, shows the main menu and exits cleanly (option 6, Ctrl+C or closed input). Also verified when launched from a different working directory. No ModuleNotFoundError, import or syntax errors.

## Unit tests (`python -m unittest discover -v`, `python -m unittest test_core -v`)
- Tests Passed: 70
- Tests Failed: 0
- Errors: 0

## Results by area
| Area | Result | How verified |
|------|--------|--------------|
| CRUD (programs, services, inquiries, inquiry status update) | PASS | unit tests + scripted runs of `main.py` |
| Search (name, category, customer, email, service; case-insensitive; no-match; empty keyword) | PASS | unit tests + scripted run |
| Filtering (Active/Inactive; Open/In Progress/Closed; invalid choice) | PASS | unit tests + scripted run |
| Reports (counts equal JSON data; category and status reports; empty data) | PASS | unit tests + scripted run |
| JSON persistence (data saved, app restarted, data still present; unique IDs; IDs not reused after delete) | PASS | unit tests + two separate `main.py` processes |
| Missing JSON files (recreated with sample data) | PASS | unit tests + deleted files in a copy |
| Corrupted JSON (no crash; file kept as `.corrupt`) | PASS | unit tests + corrupted file in a copy |
| Validation (empty input, invalid email, invalid/missing IDs, invalid status, invalid menu choices) | PASS | unit tests + scripted run |

## Not tested
- pytest (not configured in the project)
- Real interactive typing in a terminal (input was simulated with mocks and piped stdin)
- Concurrent use by multiple users or processes

## Final Status
Application Status: Working
Final Status: **PASS**
