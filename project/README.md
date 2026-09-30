# Veda Technology Business & Service Management System

A Python-based Business & Service Management System developed as part of the Veda Technology Python Programming Internship.

The project demonstrates practical Python programming concepts including functions, modules, Object-Oriented Programming, CRUD operations, JSON/CSV file handling, validation, searching, filtering, reporting, exception handling, and unit testing.

---

## Project Objectives

The system is designed to manage:

- Technology programs
- Digital services
- Customers
- Customer inquiries
- Search and filtering
- Business reports
- Persistent data storage

The project uses synthetic/sample data only.

---

## Technologies Used

- Python
- Object-Oriented Programming
- JSON
- CSV
- unittest
- File Handling
- Exception Handling
- Git
- GitHub
- VS Code

---

## Main Features

### 1. Program Management

- Add programs
- View programs
- Search programs
- Filter programs by status
- Update programs
- Delete programs
- Automatic program ID generation

### 2. Service Management

- Add services
- View services
- Search services
- Filter services by status
- Update services
- Delete services
- Automatic service ID generation

### 3. Customer / Inquiry Management

- Add customer inquiries
- View inquiries
- Search inquiries
- Filter inquiries by status
- Update inquiries
- Update inquiry status
- Delete inquiries
- Automatic inquiry ID generation

### 4. Search and Filtering

The system supports searching by:

- Program name
- Program category
- Service name
- Service category
- Customer name
- Customer email
- Inquiry service

Records can also be filtered by status.

### 5. Business Reports

The reporting module provides:

- Business summary
- Program reports
- Service reports
- Category-based reports
- Inquiry status reports
- Record counts

### 6. Data Storage

The application supports persistent storage using:

- JSON files
- CSV files

Data is stored inside the `data` directory.

### 7. Validation

The system validates:

- Empty input
- Email addresses
- Record IDs
- Status values
- Case-insensitive ID searches

### 8. Exception Handling

File-related errors and invalid JSON data are handled using exception handling so that the application can continue safely.

### 9. Unit Testing

The project uses Python's built-in `unittest` framework to test:

- ID generation
- Input validation
- Email validation
- ID searching
- Record searching
- Status validation

---

## Project Structure

```text
Veda-Business-Service-Management-System/
│
├── main.py
├── models.py
├── programs.py
├── services.py
├── inquiries.py
├── search.py
├── reports.py
├── storage.py
├── validation.py
├── test_core.py
├── README.md
├── sample_output.txt
│
└── data/
    ├── programs.json
    ├── services.json
    └── inquiries.json