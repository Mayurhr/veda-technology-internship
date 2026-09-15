# Build a Concurrent URL Checker

## Description

This project checks whether multiple URLs are available and measures how long each request takes. The checks run concurrently so that one slow URL does not make every other URL wait.

## Objective

The objective is to practice concurrency and network programming with Python.

## Tools Used

- Python
- requests
- concurrent.futures.ThreadPoolExecutor

## Features

- Check multiple URLs concurrently
- Display the HTTP status code when a response is received
- Measure the response time for every URL
- Handle successful, invalid, unreachable, and timed-out requests
- Continue checking other URLs when one request fails
- Display a final summary

## Project Structure

```text
Concurrent-URL-Checker/
├── url_checker.py
├── README.md
└── sample_output.txt
```

## How It Works

The program stores a small list of URLs and sends one request for each URL. The `check_url` function records the start time, sends the request, and returns the URL, availability, status code, response time, and error message when needed. The results are then printed in a clear report.

## Why Concurrency Is Used

Network requests spend much of their time waiting for a server response. Running the requests concurrently allows another URL to be checked during that waiting time. This makes the complete check faster than checking every URL one after another.

## ThreadPoolExecutor

`ThreadPoolExecutor` creates and manages a small group of worker threads. Each URL is submitted as a separate task. This program uses a maximum of four workers, which is enough for the small sample without creating excessive threads.

## Request Timeout

Every request has a five-second timeout. A timeout prevents the program from waiting forever for a server that does not respond.

## Failure Handling

The program catches timeout, connection, invalid URL, and other request errors. A failed URL is reported with its error message, while the remaining URL checks continue normally.

## Installation

Install the `requests` package:

```text
pip install requests
```

## How to Run

Open a terminal in this project folder and run:

```text
python url_checker.py
```

The sample list includes working websites and `https://invalid.example` to demonstrate failure handling.

## Sample Output

See `sample_output.txt` for an example report.

## Concepts Learned

- HTTP requests with Python
- URL availability checking
- Response-time measurement
- Thread-based concurrency
- ThreadPoolExecutor
- Request timeouts
- Exception handling

## Conclusion

This project demonstrates how a small Python utility can check several URLs efficiently. Concurrency improves the waiting time for I/O-bound network work, while timeouts and exception handling keep the program reliable.