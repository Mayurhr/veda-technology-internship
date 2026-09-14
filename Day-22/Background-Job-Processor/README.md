# Create a Background Job Processor

## Description

This project creates a small FastAPI application that sends time-consuming report work to a background job. The API responds quickly while the report is processed separately.

## Objective

The objective is to understand how background processing can keep a web request from waiting for a long task to finish.

## Tools Used

- Python
- FastAPI
- Uvicorn
- FastAPI BackgroundTasks
- Python logging module

## Features

- Submit a report generation job
- Generate a unique job ID
- Store jobs in memory
- Track queued, running, completed, and failed statuses
- Record job activity in `execution.log`
- Handle failed jobs with `try/except`

## Project Structure

```text
Background-Job-Processor/
├── background_job.py
├── README.md
├── sample_output.txt
└── execution.log
```

## How Background Jobs Work

The submit endpoint creates a job and gives it a unique ID. FastAPI then sends the report work to a background task. The request receives a response without waiting for the three-second processing delay. The background task updates the job status as it runs.

## Task Submission

Send a `POST` request to `/jobs`. The request body can include a report name:

```json
{"report_name": "sales_report"}
```

To demonstrate failure handling, set `force_failure` to `true`:

```json
{"report_name": "failed_report", "force_failure": true}
```

## Job Status Tracking

The response includes a job ID and the first status, which is `queued`. Use `GET /jobs/{job_id}` to check the job. The status changes to `running` and then to `completed` or `failed`.

## Error Handling

The background function uses `try/except`. If report processing fails, the job is marked as `failed` and the error message is saved with the job.

## Logging

The Python logging module writes submission, start, completion, and failure messages to `execution.log`.

## Installation

Install the required packages:

```text
pip install fastapi uvicorn
```

## How to Run

Open a terminal in this project folder and run:

```text
uvicorn background_job:app --reload
```

The API runs at `http://127.0.0.1:8000`. Press `Ctrl+C` to stop the server safely.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check that the API is running |
| POST | `/jobs` | Submit a background report job |
| GET | `/jobs/{job_id}` | Check a job's status |

## Sample Output

See `sample_output.txt` for a successful job submission and status checks.

## Concepts Learned

- Background task processing
- FastAPI endpoints
- Unique job IDs
- In-memory status tracking
- Execution logging
- Handling failed jobs
- Keeping long work out of the main response

## Conclusion

This task demonstrates a simple background job processor. FastAPI accepts a job quickly, while the background task performs the longer report operation and records its result.