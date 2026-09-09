# Email Report Automation System

## Description

This project processes a small business sales dataset and prepares a report that can be sent by email.

## Objective

The objective is to learn report generation, automation, and email integration using Python.

## Tools Used

- Python
- Pandas
- SMTP
- Logging module
- Environment variables

## Features

- Creates a sample business dataset
- Calculates useful sales information
- Generates a formatted business report
- Sends the report through email when configured
- Skips email safely when credentials are missing
- Records program activity in a log file

## How the Program Works

The program creates four sales records using Pandas. It processes the records, creates the report, and then tries to send the report by email. The program can still finish successfully when email settings are not available.

## Report Generation

The report shows the number of records, total sales, total quantity, average sales, and highest-selling product.

## Email Automation

The `send_email()` function uses Python SMTP to connect to an email server. It sends the report as the email message after the required settings are found.

## Environment Variables

Email credentials are not stored in the program. The following environment variables can be used:

- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`
- `EMAIL_TO`

Do not add real passwords or credentials to this repository.

## Logging

The program uses Python's `logging` module to write events to `execution.log`. It records when the program starts, the report is generated, email activity occurs, and the program completes.

## Error Handling

The program uses `try/except` to handle report and email errors. Email errors are logged and displayed without stopping report generation.

## Installation

Install the required packages with:

```text
pip install pandas openpyxl
```

`openpyxl` is included for Excel report support if the report is extended later.

## How to Run

Open this project folder and run:

```text
python email_report_automation.py
```

For email sending, configure the environment variables before running the program. Without them, the report is generated and email is skipped safely.

## Sample Output

See `sample_output.txt` for a successful report generation example with email safely skipped when credentials are not configured.

## Concepts Learned

- Pandas DataFrames
- Report generation
- SMTP email automation
- Environment variables
- Logging
- Error handling

## Conclusion

This task demonstrated how Python can process business data, create a useful report, and prepare it for automatic email delivery without storing sensitive credentials in the code.
