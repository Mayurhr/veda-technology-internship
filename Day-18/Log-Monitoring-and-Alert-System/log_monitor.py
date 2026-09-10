import logging
import os
import re


PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(PROJECT_FOLDER, "sample_log.txt")
ALERT_FILE = os.path.join(PROJECT_FOLDER, "alert.log")
EXECUTION_FILE = os.path.join(PROJECT_FOLDER, "execution.log")
ERROR_THRESHOLD = 3

logging.basicConfig(
    filename=EXECUTION_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def monitor_log_file():
    logging.info("Monitoring started")
    print("Log Monitoring Started")

    try:
        if not os.path.exists(LOG_FILE):
            logging.error("Log file is missing: %s", LOG_FILE)
            print("Log file not found. Monitoring stopped safely.")
            return

        print("Checking sample_log.txt...")
        with open(LOG_FILE, "r", encoding="utf-8") as log_file:
            log_content = log_file.read()

        error_entries = re.findall(r"\bERROR\b", log_content)
        error_count = len(error_entries)
        logging.info("Log file checked: %s", LOG_FILE)
        logging.info("Number of errors found: %s", error_count)
        logging.info("Error threshold: %s", ERROR_THRESHOLD)

        print(f"Total ERROR entries found: {error_count}")
        print(f"Error threshold: {ERROR_THRESHOLD}")

        if error_count >= ERROR_THRESHOLD:
            alert_message = "\n".join(
                [
                    "ALERT: Error count reached the configured threshold.",
                    f"Total errors: {error_count}",
                    f"Threshold: {ERROR_THRESHOLD}",
                ]
            )
            with open(ALERT_FILE, "w", encoding="utf-8") as alert_file:
                alert_file.write(alert_message + "\n")

            logging.warning("Alert generated")
            print("ALERT: Error threshold reached!")
            print("Alert saved to alert.log")
        else:
            logging.info("No alert generated")
            print("No alert generated. Error count is below the threshold.")

        logging.info("Monitoring completed")
        print("Monitoring completed successfully.")
    except OSError as error:
        logging.error("File reading error: %s", error)
        print(f"File reading error handled safely: {error}")
    except Exception as error:
        logging.error("Unexpected error: %s", error)
        print(f"Unexpected error handled safely: {error}")


if __name__ == "__main__":
    monitor_log_file()