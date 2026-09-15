import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://httpbin.org/status/200",
    "https://invalid.example",
]
MAX_WORKERS = 4
REQUEST_TIMEOUT = 5


def check_url(url, timeout=REQUEST_TIMEOUT):
    """Check one URL and return its status and response time."""
    start_time = time.perf_counter()

    try:
        response = requests.get(url, timeout=timeout)
        response_time = time.perf_counter() - start_time
        return {
            "url": url,
            "available": response.ok,
            "status_code": response.status_code,
            "response_time": response_time,
            "error": "",
        }
    except requests.exceptions.Timeout:
        error = "Request timed out"
    except requests.exceptions.ConnectionError:
        error = "Connection error"
    except requests.exceptions.InvalidURL:
        error = "Invalid URL"
    except requests.exceptions.RequestException as request_error:
        error = str(request_error)

    response_time = time.perf_counter() - start_time
    return {
        "url": url,
        "available": False,
        "status_code": None,
        "response_time": response_time,
        "error": error,
    }


def check_urls(urls):
    """Check several URLs concurrently and return results in input order."""
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls}

        for future in as_completed(future_to_url):
            results.append(future.result())

    return sorted(results, key=lambda result: urls.index(result["url"]))


def print_report(results):
    """Print the URL results and a final summary."""
    print("Concurrent URL Checker")
    print("=" * 70)

    successful_urls = 0

    for result in results:
        if result["available"]:
            successful_urls += 1
            status = f"Available (HTTP {result['status_code']})"
        else:
            status = f"Failed ({result['error']})"

        print(f"URL: {result['url']}")
        print(f"Status: {status}")
        print(f"Response time: {result['response_time']:.2f} seconds")
        print("-" * 70)

    failed_urls = len(results) - successful_urls
    response_times = [result["response_time"] for result in results]
    average_time = sum(response_times) / len(response_times) if response_times else 0

    print("Summary")
    print(f"Total URLs checked: {len(results)}")
    print(f"Successful URLs: {successful_urls}")
    print(f"Failed URLs: {failed_urls}")
    print(f"Average response time: {average_time:.2f} seconds")


if __name__ == "__main__":
    print_report(check_urls(URLS))