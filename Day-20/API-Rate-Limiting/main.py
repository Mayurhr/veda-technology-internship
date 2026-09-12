import math
import time

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status


MAX_REQUESTS = 5
WINDOW_SECONDS = 60
request_history = {}

app = FastAPI(title="API Rate Limiting")


def check_rate_limit(request: Request, response: Response):
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.monotonic()
    recent_requests = request_history.get(client_ip, [])

    recent_requests = [
        request_time
        for request_time in recent_requests
        if current_time - request_time < WINDOW_SECONDS
    ]

    if len(recent_requests) >= MAX_REQUESTS:
        retry_after = math.ceil(WINDOW_SECONDS - (current_time - recent_requests[0]))
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
            headers={
                "X-RateLimit-Limit": str(MAX_REQUESTS),
                "X-RateLimit-Remaining": "0",
                "Retry-After": str(retry_after),
            },
        )

    recent_requests.append(current_time)
    request_history[client_ip] = recent_requests
    response.headers["X-RateLimit-Limit"] = str(MAX_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(
        MAX_REQUESTS - len(recent_requests)
    )


@app.get("/hello", dependencies=[Depends(check_rate_limit)])
def hello():
    return {"message": "Hello! Your request was accepted."}