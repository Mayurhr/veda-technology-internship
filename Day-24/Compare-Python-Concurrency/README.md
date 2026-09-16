# Compare Threading, Multiprocessing, and AsyncIO

## Description

This project contains simple Python examples that compare Threading, Multiprocessing, and AsyncIO using suitable workloads.

The purpose is to understand how different concurrency approaches work in Python.

## Objective

Understand when different Python concurrency approaches should be used.

## Tools Used

- Python
- threading
- multiprocessing
- asyncio
- time

## Features

- Threading example for I/O-bound work
- Multiprocessing example for CPU-bound work
- AsyncIO example for I/O-bound work
- Execution-time measurement
- Simple result comparison

## Implementation

### Threading

The threading program creates multiple threads and performs an I/O-style task using a one-second wait.

### Multiprocessing

The multiprocessing program creates separate processes and performs a CPU-intensive calculation.

### AsyncIO

The AsyncIO program creates asynchronous tasks and runs multiple I/O-style tasks concurrently.

## How to Run

Run the programs separately using:

```bash
python threading_example.py
