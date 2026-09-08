import logging
import time
from pathlib import Path

import schedule


PROJECT_FOLDER = Path(__file__).parent
REPORT_FILE = PROJECT_FOLDER / "output_report.txt"
LOG_FILE = PROJECT_FOLDER / "execution.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def process_data(data):
    total = sum(item["amount"] for item in data)
    average = total / len(data)
    return total, average


def create_report(data, total, average):
    with REPORT_FILE.open("w", encoding="utf-8") as report:
        report.write("Scheduled Data Job Report\n")
        report.write("-------------------------\n")
        report.write(f"Records processed: {len(data)}\n")
        report.write(f"Total sales: ${total:.2f}\n")
        report.write(f"Average sale: ${average:.2f}\n")


def run_job():
    data = [
        {"item": "Notebook", "amount": 120.00},
        {"item": "Pen Set", "amount": 45.50},
        {"item": "Desk Organizer", "amount": 84.50},
    ]

    logging.info("Job started")
    try:
        total, average = process_data(data)
        create_report(data, total, average)
        logging.info("Job completed successfully")
        print("Job completed successfully")
        print(f"Processed data: {len(data)} records")
        print(f"Total: ${total:.2f}")
        print(f"Average: ${average:.2f}")
    except Exception as error:
        logging.error("Job failed: %s", error)
        print(f"Job failed: {error}")


def main():
    print("Program started")
    print("Running the first job execution...")
    run_job()
    schedule.every(10).seconds.do(run_job)
    print("Scheduler running. The job will run every 10 seconds.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Job stopped")
        print("Scheduler stopped safely")


if __name__ == "__main__":
    main()