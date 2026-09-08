# Scheduled Python Data Job

## Description

This project is a Python program that processes a small sales dataset and runs the job automatically on a schedule.

## Objective

Learn how to schedule a Python data task, create a report, and record its execution with logging.

## Tools Used

- Python
- Schedule library
- Logging module

## Features

- Uses a sample dataset created in Python
- Calculates total and average sales
- Creates an output report
- Runs the job every 10 seconds
- Logs successful and failed executions
- Stops safely with Ctrl+C

## How the Scheduled Job Works

The program processes three sales records in the `run_job()` function. It calculates the total and average amount, then writes the results to `output_report.txt`. The first job runs when the program starts, and the schedule library runs it again at the defined interval.

## Scheduling Configuration

The job is scheduled with `schedule.every(10).seconds.do(run_job)`. The loop checks for pending jobs every second.

## Logging

The Python logging module writes job started, successful completion, failed execution, and stopped messages to `execution.log`.

## Error Handling

The job uses `try/except` so a failed execution is logged and printed without stopping the scheduler.

## How to Install Requirements

Install the Schedule library with:

```text
pip install schedule
```

## How to Run

Open this project folder and run:

```text
python scheduled_data_job.py
```

Press Ctrl+C to stop the scheduler safely.

## Sample Output

See `sample_output.txt` for an example of a successful run. The generated report is saved in `output_report.txt`.

## Concepts Learned

- Functions
- Dataset processing
- File writing
- Scheduling jobs
- Logging
- Error handling
- Safe program shutdown

## Conclusion

This task demonstrated how a simple Python data job can run repeatedly on a schedule and create a report while keeping an execution log.