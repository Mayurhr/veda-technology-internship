import json
import os
import time

import redis
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "30"))
CACHE_KEY = "sample_api_data"

app = FastAPI(title="API Caching Layer")
redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
)

sample_data = {
    "message": "This data came from the sample API.",
    "version": 1,
}


class DataUpdate(BaseModel):
    message: str


def get_redis_client():
    try:
        redis_client.ping()
        return redis_client
    except redis.exceptions.RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis is unavailable. Start Redis and try again.",
        ) from error


def fetch_data_from_source():
    time.sleep(0.05)
    return sample_data.copy()


@app.get("/")
def read_root():
    return {"message": "API Caching Layer is running."}


@app.get("/data")
def get_data():
    start_time = time.perf_counter()
    client = get_redis_client()

    try:
        cached_data = client.get(CACHE_KEY)
        if cached_data:
            data = json.loads(cached_data)
            cache_status = "hit"
        else:
            data = fetch_data_from_source()
            client.setex(CACHE_KEY, CACHE_TTL_SECONDS, json.dumps(data))
            cache_status = "miss"
    except (redis.exceptions.RedisError, json.JSONDecodeError) as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The API could not read or write the Redis cache.",
        ) from error

    response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
    return {
        "data": data,
        "cache_status": cache_status,
        "cache_ttl_seconds": CACHE_TTL_SECONDS,
        "response_time_ms": response_time_ms,
    }


@app.put("/data")
def update_data(update: DataUpdate):
    global sample_data

    sample_data = {
        "message": update.message,
        "version": sample_data["version"] + 1,
    }
    invalidate_cache()
    return {
        "message": "Underlying data updated and related cache invalidated.",
        "data": sample_data,
    }


@app.delete("/cache/data")
def invalidate_cache():
    client = get_redis_client()
    try:
        client.delete(CACHE_KEY)
    except redis.exceptions.RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The API could not invalidate the Redis cache.",
        ) from error
    return {"message": "Cache invalidated successfully."}


@app.get("/performance")
def compare_performance():
    client = get_redis_client()
    try:
        client.delete(CACHE_KEY)

        uncached_start = time.perf_counter()
        fetch_data_from_source()
        uncached_time_ms = round((time.perf_counter() - uncached_start) * 1000, 2)

        client.setex(CACHE_KEY, CACHE_TTL_SECONDS, json.dumps(sample_data))
        cached_start = time.perf_counter()
        client.get(CACHE_KEY)
        cached_time_ms = round((time.perf_counter() - cached_start) * 1000, 2)
    except redis.exceptions.RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The performance test requires an available Redis server.",
        ) from error

    return {
        "uncached_response_time_ms": uncached_time_ms,
        "cached_response_time_ms": cached_time_ms,
        "result": "Cached response avoids repeated data retrieval.",
    }
