# Log Monitoring and Alert System

## Description

This project checks a log file for ERROR entries and creates an alert when too many errors are found.

## Objective

The objective is to practice file processing, regular expressions, logging, and simple automation.

## Tools Used

- Python
- Regular expressions
- Logging module
- `os` module

## Features

- Reads a sample log file
- Finds ERROR entries using a regular expression
- Counts the errors
- Uses a configurable error threshold
- Saves and displays an alert
- Records program activity in a log file

## How the Program Works

The program opens `sample_log.txt` and reads its log entries. It searches for the word `ERROR`, counts the matches, and compares the count with `ERROR_THRESHOLD`. It creates an alert when the threshold is reached.

## Error Pattern Detection

The program uses the regular expression `\bERROR\b` to identify complete ERROR words in the log file.

## Configurable Threshold

The error threshold is stored in the `ERROR_THRESHOLD` variable near the top of the program. It can be changed easily, for example from `3` to `4`.

## Alert Mechanism

When the number of errors reaches the threshold, the program displays an alert in the terminal and saves the alert details in `alert.log`.

## Logging

The program uses Python's `logging` module to record monitoring events in `execution.log`, including the file check, error count, threshold, alert, and completion.

## Error Handling

The program handles a missing log file, file reading errors, and unexpected errors using `try/except`. These problems are displayed and recorded without crashing the program unnecessarily.

## How to Run

Open the project folder and run:

```text
python log_monitor.py
```

## Sample Output

See `sample_output.txt` for an example of a successful run.

## Concepts Learned

- Reading text files
- Regular expression pattern matching
- Counting matching entries
- Configurable thresholds
- Alert generation
- Python logging
- Error handling

## Conclusion

This task demonstrated how Python can monitor a log file and provide an alert when the number of errors becomes too high.