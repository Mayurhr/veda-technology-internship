# Retry and Timeout System for API Calls

## Description

This project creates a reusable API client with request timeouts, retry logic, exponential backoff, logging, and clear failure handling.

## Objective

The objective is to practice resilient API communication that can handle temporary network problems without retrying permanent client errors.

## Tools Used

- Python
- requests
- logging

## Features

- Request timeout
- Maximum retry count
- Exponential backoff
- Retryable error handling
- Logging
- Failure handling
- Reusable API client

## How It Works

The `APIClient` sends a request with a configured timeout. It returns successful responses immediately. When a connection error, timeout, or temporary server response occurs, it waits and tries again. When retries are exhausted, it raises a clear `APIRequestError` that the program handles safely.

## Retry Strategy

The client retries connection errors, timeout errors, and HTTP status codes 429, 500, 502, 503, and 504. It does not retry normal client errors such as 400, 401, 403, or 404 because repeating those requests will not normally fix the problem.

## Exponential Backoff

The delay uses this formula:

```text
delay = backoff_factor * (2 ** (attempt - 1))
```

With a backoff factor of `0.5`, retry delays are 0.5 seconds, 1.0 seconds, and 2.0 seconds.

## Timeout Configuration

The `REQUEST_TIMEOUT` value near the top of `retry_api_client.py` controls how many seconds the client waits for each request. A timeout prevents the program from waiting forever for an unavailable API.

## Error Handling

Network timeouts and connection errors are caught and retried when attempts remain. Non-retryable HTTP errors fail immediately. If every allowed attempt fails, the client raises `APIRequestError`, and the demo prints an understandable message instead of crashing.

## Logging

The program writes request starts, attempt numbers, timeout values, retry reasons, retry delays, successful responses, and final failures to `execution.log`.

## Installation

```text
pip install requests
```

## How to Run

Open a terminal in this project folder and run:

```text
python retry_api_client.py
```

The demo uses the public `https://httpbin.org` API. It makes a successful request and then calls a temporary `503` endpoint to demonstrate retries.

## Sample Output

The output below is an example, not an exact live result. Network timing and timestamps can be different when the program runs.

```text
Request started: GET https://httpbin.org/get
Successful request: HTTP 200
Request started: GET https://httpbin.org/status/503
Retrying after HTTP 503 - retry=1 delay=0.5 seconds
Retrying after HTTP 503 - retry=2 delay=1.0 seconds
Retrying after HTTP 503 - retry=3 delay=2.0 seconds
Temporary failure handled: HTTP 503
```

## Concepts Learned

- API requests
- Timeouts
- Retry logic
- Exponential backoff
- HTTP status codes
- Exception handling
- Logging
- Resilient network programming

## Conclusion

This project demonstrates how timeouts, selective retries, increasing delays, and logging make API calls more reliable and easier to understand when temporary failures occur.
