import logging
import time
from pathlib import Path

import requests


BASE_URL = "https://httpbin.org"
REQUEST_TIMEOUT = 5
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.5
LOG_FILE = Path(__file__).with_name("execution.log")

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


logger = logging.getLogger("retry_api_client")
logger.setLevel(logging.INFO)
logger.propagate = False
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)


class APIRequestError(Exception):
    """Raised when an API request cannot be completed."""


class APIClient:
    """Reusable API client with timeout and retry support."""

    def __init__(self, base_url=BASE_URL, timeout=REQUEST_TIMEOUT,
                 max_retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = requests.Session()

    def request(self, method, endpoint, **kwargs):
        """Send an API request and retry only temporary failures."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info("Request started - method=%s url=%s", method.upper(), url)

        for attempt in range(1, self.max_retries + 2):
            logger.info("Attempt %s - timeout=%s seconds", attempt, self.timeout)

            try:
                response = self.session.request(
                    method,
                    url,
                    timeout=self.timeout,
                    **kwargs,
                )

                if response.status_code not in RETRYABLE_STATUS_CODES:
                    response.raise_for_status()
                    logger.info(
                        "Successful response - status=%s attempt=%s",
                        response.status_code,
                        attempt,
                    )
                    return response

                error_message = f"HTTP {response.status_code}"
                if attempt > self.max_retries:
                    raise APIRequestError(error_message)

                self._wait_before_retry(attempt, error_message)
            except requests.exceptions.Timeout as error:
                if attempt > self.max_retries:
                    raise APIRequestError(
                        f"Request timed out after {attempt} attempts."
                    ) from error
                self._wait_before_retry(attempt, "request timeout")
            except requests.exceptions.ConnectionError as error:
                if attempt > self.max_retries:
                    raise APIRequestError(
                        f"Connection failed after {attempt} attempts."
                    ) from error
                self._wait_before_retry(attempt, "connection error")
            except requests.exceptions.HTTPError as error:
                raise APIRequestError(
                    f"Request failed with non-retryable status "
                    f"{error.response.status_code}."
                ) from error
            except requests.exceptions.RequestException as error:
                raise APIRequestError(f"Request failed: {error}") from error

        raise APIRequestError("Request failed after all retry attempts.")

    def _wait_before_retry(self, attempt, reason):
        delay = self.backoff_factor * (2 ** (attempt - 1))
        logger.warning(
            "Retrying after %s - retry=%s delay=%.1f seconds",
            reason,
            attempt,
            delay,
        )
        time.sleep(delay)

    def get(self, endpoint, **kwargs):
        """Send a GET request."""
        return self.request("GET", endpoint, **kwargs)


def run_demo():
    """Run one successful request and one temporary failure example."""
    client = APIClient()

    try:
        response = client.get("/get")
        print(f"Successful request: HTTP {response.status_code}")
    except APIRequestError as error:
        logger.error("Final failure - %s", error)
        print(f"Successful request failed: {error}")

    try:
        client.get("/status/503")
    except APIRequestError as error:
        logger.error("Final failure - %s", error)
        print(f"Temporary failure handled: {error}")


if __name__ == "__main__":
    run_demo()
