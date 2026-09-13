# Build a Caching Layer for an API

## Description

This project adds a Redis caching layer to a simple FastAPI application. The API returns sample data and records whether the response came from Redis or from the data source.

## Objective

The objective is to understand how caching can reduce repeated data retrieval and improve API response time.

## Tools Used

- Python
- FastAPI
- Redis
- Uvicorn

## Features

- Simple FastAPI application
- Redis cache for frequently requested sample data
- Cache hit and cache miss messages
- Configurable cache expiration time
- Cache invalidation after underlying data changes
- Performance comparison endpoint
- Clear error response when Redis is unavailable

## Project Structure

```text
API-Caching-Layer/
├── api_cache.py
├── README.md
├── sample_output.txt
└── performance_comparison.txt
```

## How Caching Works

When `/data` is requested, the application checks Redis first. If the data is cached, it returns the cached response as a cache hit. If the data is not cached, the application retrieves the data, stores it in Redis, and returns it as a cache miss.

## Cache Configuration

The Redis connection URL is read from the `REDIS_URL` environment variable. The default value is `redis://localhost:6379/0`.

The cache key is `sample_api_data`.

## Cache Expiration

The default cache expiration time is 30 seconds. It is read from `CACHE_TTL_SECONDS` and can be changed without editing the Python file.

Example in PowerShell:

```text
$env:CACHE_TTL_SECONDS = "10"
```

After the expiration time, Redis removes the cached value and the next request is a cache miss.

## Cache Invalidation

`PUT /data` changes the underlying sample data and deletes the related Redis key immediately. `DELETE /cache/data` also provides a direct cache invalidation endpoint. The next `/data` request retrieves fresh data and stores it again.

## Before and After Performance

`GET /performance` compares retrieving data from the source with reading the same data from Redis. The measured example is saved in `performance_comparison.txt`. The exact times can change depending on the computer and Redis connection.

## Installation

Open the project folder and install the requirements:

```text
pip install fastapi uvicorn redis
```

Redis must also be installed and running locally, or a Redis server must be available at the URL in `REDIS_URL`. The Python package alone does not start the Redis server.

## How to Run

Start Redis first, then run the API:

```text
uvicorn api_cache:app --reload
```

The API runs at `http://127.0.0.1:8000` by default. Press `Ctrl+C` to stop Uvicorn safely.

If Redis is unavailable, the API can start, but data and cache requests return HTTP 503 with a clear Redis error message.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check that the API is running |
| GET | `/data` | Get sample data with cache status |
| PUT | `/data` | Change data and invalidate its cache |
| DELETE | `/cache/data` | Invalidate the sample data cache |
| GET | `/performance` | Compare uncached and cached response times |

## Sample Output

See `sample_output.txt` for a successful example of startup, cache miss, cache hit, invalidation, and performance testing.

## Concepts Learned

- Redis key-value caching
- Cache hits and cache misses
- Cache expiration with TTL
- Cache invalidation after data changes
- FastAPI endpoints and HTTP status codes
- Basic response time measurement
- Graceful handling of service errors

## Conclusion

This task demonstrates a simple Redis caching layer for a FastAPI application. Caching avoids repeated data retrieval, while expiration and invalidation help keep cached data current.
