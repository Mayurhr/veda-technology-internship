import sys
from datetime import date
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "sample_data.csv"
PDF_FILE = BASE_DIR / "generated_report.pdf"
SUMMARY_FILE = BASE_DIR / "sample_output.txt"
REPORT_TITLE = "Quarterly Sales Report"
REQUIRED_COLUMNS = ["Order ID", "Date", "Product", "Category", "Region", "Units", "Unit Price"]
HEADER_COLOR = colors.HexColor("#1F3A5F")
ROW_COLOR = colors.HexColor("#EEF2F7")


def money(value):
    return f"${value:,.2f}"


def load_data(csv_path):
    data = pd.read_csv(csv_path)

    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    data = data.dropna(subset=REQUIRED_COLUMNS)
    data = data.drop_duplicates(subset="Order ID")
    if data.empty:
        raise ValueError("The CSV file has no usable records.")

    data["Date"] = pd.to_datetime(data["Date"])
    data["Revenue"] = data["Units"] * data["Unit Price"]
    return data.sort_values("Date").reset_index(drop=True)


def calculate_metrics(data):
    product_revenue = data.groupby("Product")["Revenue"].sum()
    region_revenue = data.groupby("Region")["Revenue"].sum()
    category_revenue = data.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    total_revenue = data["Revenue"].sum()

    return {
        "start_date": data["Date"].min().strftime("%d %b %Y"),
        "end_date": data["Date"].max().strftime("%d %b %Y"),
        "total_orders": len(data),
        "total_units": int(data["Units"].sum()),
        "total_revenue": total_revenue,
        "average_order_value": total_revenue / len(data),
        "top_product": product_revenue.idxmax(),
        "top_product_revenue": product_revenue.max(),
        "top_region": region_revenue.idxmax(),
        "top_region_revenue": region_revenue.max(),
        "category_revenue": category_revenue,
    }


def build_summary_lines(metrics):
    lines = [
        f"Report Period: {metrics['start_date']} to {metrics['end_date']}",
        f"Total Orders: {metrics['total_orders']}",
        f"Total Units Sold: {metrics['total_units']}",
        f"Total Revenue: {money(metrics['total_revenue'])}",
        f"Average Order Value: {money(metrics['average_order_value'])}",
        f"Top Product: {metrics['top_product']} ({money(metrics['top_product_revenue'])})",
        f"Top Region: {metrics['top_region']} ({money(metrics['top_region_revenue'])})",
        "Revenue by Category:",
    ]
    for category, revenue in metrics["category_revenue"].items():
        lines.append(f"  {category}: {money(revenue)}")
    return lines


def styled_table(rows, column_widths, right_aligned_columns=()):
    table = Table(rows, colWidths=column_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_COLOR]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for column in right_aligned_columns:
        style.append(("ALIGN", (column, 0), (column, -1), "RIGHT"))
    table.setStyle(TableStyle(style))
    return table


def add_page_number(canvas, document):
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1 * cm, f"Page {document.page}")


def build_report(data, metrics, pdf_path):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("ReportTitle", parent=styles["Title"], textColor=HEADER_COLOR)
    heading_style = ParagraphStyle("ReportHeading", parent=styles["Heading2"], textColor=HEADER_COLOR, spaceBefore=14)

    story = [
        Paragraph(REPORT_TITLE, title_style),
        Paragraph(f"Report Date: {date.today().strftime('%d %B %Y')}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("Summary", heading_style),
        Paragraph(
            f"This report covers {metrics['total_orders']} orders placed between "
            f"{metrics['start_date']} and {metrics['end_date']}. "
            f"A total of {metrics['total_units']} units were sold, generating "
            f"{money(metrics['total_revenue'])} in revenue.",
            styles["Normal"],
        ),
        Paragraph("Summary Metrics", heading_style),
    ]

    metric_rows = [
        ["Metric", "Value"],
        ["Total Orders", metrics["total_orders"]],
        ["Total Units Sold", metrics["total_units"]],
        ["Total Revenue", money(metrics["total_revenue"])],
        ["Average Order Value", money(metrics["average_order_value"])],
        ["Top Product", f"{metrics['top_product']} ({money(metrics['top_product_revenue'])})"],
        ["Top Region", f"{metrics['top_region']} ({money(metrics['top_region_revenue'])})"],
    ]
    story.append(styled_table(metric_rows, [6 * cm, 8 * cm]))

    story.append(Paragraph("Revenue by Category", heading_style))
    category_rows = [["Category", "Revenue"]]
    for category, revenue in metrics["category_revenue"].items():
        category_rows.append([category, money(revenue)])
    story.append(styled_table(category_rows, [6 * cm, 8 * cm], right_aligned_columns=[1]))

    story.append(Paragraph("Business Data", heading_style))
    data_rows = [["Order ID", "Date", "Product", "Category", "Region", "Units", "Unit Price", "Revenue"]]
    for _, row in data.iterrows():
        data_rows.append([
            row["Order ID"],
            row["Date"].strftime("%Y-%m-%d"),
            row["Product"],
            row["Category"],
            row["Region"],
            int(row["Units"]),
            money(row["Unit Price"]),
            money(row["Revenue"]),
        ])
    widths = [2.2 * cm, 2.3 * cm, 3.6 * cm, 2.4 * cm, 1.7 * cm, 1.3 * cm, 1.8 * cm, 2.2 * cm]
    story.append(styled_table(data_rows, widths, right_aligned_columns=[5, 6, 7]))

    story.append(Paragraph("Conclusion", heading_style))
    top_category = metrics["category_revenue"].idxmax()
    story.append(Paragraph(
        f"{metrics['top_product']} was the best-performing product with "
        f"{money(metrics['top_product_revenue'])} in revenue, and the {metrics['top_region']} region "
        f"led all regions with {money(metrics['top_region_revenue'])}. "
        f"{top_category} was the strongest category. "
        f"With an average order value of {money(metrics['average_order_value'])}, "
        f"the business should keep focusing on its top products and strongest regions.",
        styles["Normal"],
    ))

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=REPORT_TITLE,
    )
    document.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def generate_report(csv_path, pdf_path, summary_path):
    print(f"Loading data from {csv_path.name}...")
    data = load_data(csv_path)
    print(f"Loaded {len(data)} records.")

    print("Calculating summary metrics...")
    metrics = calculate_metrics(data)
    summary_lines = build_summary_lines(metrics)

    print("Generating PDF report...")
    build_report(data, metrics, pdf_path)
    print(f"PDF report saved: {pdf_path.name}")

    output_lines = [REPORT_TITLE, f"Report Date: {date.today().strftime('%d %B %Y')}", ""] + summary_lines
    summary_path.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print(f"Summary saved: {summary_path.name}")

    print()
    print("\n".join(summary_lines))


def main():
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else CSV_FILE

    try:
        generate_report(csv_path, PDF_FILE, SUMMARY_FILE)
    except FileNotFoundError:
        print(f"Error: file not found - {csv_path}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: {csv_path.name} is empty.")
        sys.exit(1)
    except PermissionError:
        print("Error: could not write the output files. Close the PDF if it is open and try again.")
        sys.exit(1)
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)

    print("\nReport generation completed successfully.")


if __name__ == "__main__":
    main()
