# Veda Technology Business & Service Management System

**Veda Technology Python Programming Internship — Major Project — Day 2 of 4**

## Description

A Python-based command-line application that represents the core operations of a technology and digital-services organization.

The system manages training programs, digital services, and customer inquiries using reusable Python modules and JSON-based persistent storage.

Day 2 continues the foundation created on Day 1 by adding more complete CRUD operations, improved searching and filtering, business reports, stronger validation, and additional unit tests.

The existing Day 1 functionality is preserved and extended instead of rebuilding the project from scratch.

## Objective

Apply Python programming concepts to a realistic technology-business scenario, including:

- Functions
- Modules
- Classes and dictionaries
- Lists
- File handling
- JSON data storage
- Input validation
- CRUD operations
- Searching and filtering
- Basic business reporting
- Unit testing

## Tools Used

- Python 3
- VS Code
- JSON
- Git
- GitHub
- Python unittest

No external Python packages are required.

## Features

### Program Management

Supports:

- Add Program
- View Programs
- Search Programs
- Search by name or category
- Filter programs by status
- Update Program
- Delete Program

Each program contains:

- `program_id`
- `program_name`
- `category`
- `duration`
- `status`

Program IDs are generated automatically, for example:

```text
PRG001
PRG002
PRG003