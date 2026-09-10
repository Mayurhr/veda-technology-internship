import logging
import os
import smtplib
import ssl
from email.message import EmailMessage

import pandas as pd


PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(PROJECT_FOLDER, "execution.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_dataset():
    return pd.DataFrame(
        [
            {"Product": "Notebook", "Quantity": 10, "Sales": 120.00},
            {"Product": "Pen Set", "Quantity": 15, "Sales": 75.00},
            {"Product": "Desk Organizer", "Quantity": 5, "Sales": 150.00},
            {"Product": "File Folder", "Quantity": 8, "Sales": 80.00},
        ]
    )


def create_report(data):
    total_sales = data["Sales"].sum()
    total_quantity = data["Quantity"].sum()
    average_sales = data["Sales"].mean()
    highest_product = data.loc[data["Sales"].idxmax(), "Product"]

    report = "\n".join(
        [
            "Business Sales Report",
            "----------------------",
            f"Records processed: {len(data)}",
            f"Total sales: ${total_sales:.2f}",
            f"Total quantity: {total_quantity}",
            f"Average sales: ${average_sales:.2f}",
            f"Highest-selling product: {highest_product}",
        ]
    )
    return report


def send_email(report):
    host = os.getenv("EMAIL_HOST")
    port_value = os.getenv("EMAIL_PORT")
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    recipient = os.getenv("EMAIL_TO")

    if not all([host, port_value, username, password, recipient]):
        logging.info("Email skipped because credentials are not configured")
        print("Email status: Skipped (email credentials are not configured)")
        return False

    logging.info("Email sending attempt")
    try:
        port = int(port_value)
        message = EmailMessage()
        message["Subject"] = "Business Sales Report"
        message["From"] = username
        message["To"] = recipient
        message.set_content(report)

        context = ssl.create_default_context()
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.starttls(context=context)
            server.login(username, password)
            server.send_message(message)

        logging.info("Email sent successfully")
        print("Email status: Sent successfully")
        return True
    except Exception as error:
        logging.error("Email failure: %s", error)
        print(f"Email status: Failed ({error})")
        return False


def main():
    logging.info("Program started")
    print("Program started")

    try:
        data = create_dataset()
        print(f"Dataset processed: {len(data)} records")
        report = create_report(data)
        logging.info("Report generated")
        print(report)
        print("Report generated successfully")
        send_email(report)
        logging.info("Program completed")
        print("Program completed")
    except Exception as error:
        logging.error("Program failed: %s", error)
        print(f"Program failed: {error}")


if __name__ == "__main__":
    main()
