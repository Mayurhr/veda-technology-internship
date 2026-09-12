# API Rate Limiting

## Description

This project adds basic rate limiting to a FastAPI endpoint. It limits the number of requests that one client can make during a fixed time window.

## Objective

The objective is to understand how API rate limiting can improve API reliability and help prevent excessive requests from individual clients.

## Tools Used

- Python
- FastAPI
- In-memory storage
- Uvicorn

## Project Structure

```text
API-Rate-Limiting/
├── main.py
├── requirements.txt
├── README.md
└── sample_output.txt
```

## Features

- FastAPI application
- `GET /hello` test endpoint
- Configurable request limit
- Separate request tracking for each client IP address
- HTTP 429 response when the limit is exceeded
- Remaining request and retry information in response headers
- Automatic counter expiration after the time window

## What Is API Rate Limiting

API rate limiting controls how many requests a client can make in a period of time. It helps protect an API from excessive traffic and allows server resources to be shared fairly.

## How the Rate Limiter Works

The application stores request times in a Python dictionary. Each client IP address is used as a key, and its recent request times are stored in a list. Before accepting a request, old timestamps are removed and the remaining timestamps are counted.

## Request Limit

The default limit is stored in `MAX_REQUESTS`:

```text
MAX_REQUESTS = 5
```

A client can make five accepted requests during the configured time window.

## Time Window

The default time window is stored in `WINDOW_SECONDS`:

```text
WINDOW_SECONDS = 60
```

Requests older than 60 seconds are removed from the client's history.

## Client Identification

The client IP address from the FastAPI request is used as the basic client identifier. Different IP addresses have separate counters.

## HTTP 429 Response

The sixth request within the time window returns HTTP status code `429 Too Many Requests` with this message:

```text
Rate limit exceeded. Please try again later.
```

The response also includes `Retry-After`, `X-RateLimit-Limit`, and `X-RateLimit-Remaining` headers.

## Counter Expiration and Reset

When the time window expires, old request timestamps are removed. The client can then make new requests normally without restarting the application.

## Testing

The API was tested with multiple requests to `/hello`. The test covered requests within the limit, the request reaching the limit, an exceeding request with HTTP 429, and a request accepted after the time window expired.

## Installation

Open the project folder and install the requirements:

```text
pip install -r requirements.txt
```

## How to Run

```text
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000` by default.

## How to Test the API

Open another terminal in the project folder and send several requests:

```text
curl -i http://127.0.0.1:8000/hello
```

Send the request six times quickly. The first five requests succeed, and the sixth request returns HTTP 429. After 60 seconds, the counter resets.

## Sample Output

See `sample_output.txt` for realistic results from testing the endpoint.

## Concepts Learned

- FastAPI endpoints and dependencies
- In-memory dictionaries and lists
- Client identification using IP addresses
- Configurable request limits
- Time windows and timestamp expiration
- HTTP 429 Too Many Requests
- Response headers for rate limit information

## Conclusion

This task demonstrated a simple in-memory rate limiter for a FastAPI endpoint. It showed how to limit requests per client and reset the counter after a configured time window.