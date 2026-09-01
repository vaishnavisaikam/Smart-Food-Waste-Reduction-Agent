from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os


# ------------------------------------------------
# REGISTER UNICODE FONT
# ------------------------------------------------

font_path = "C:/Windows/Fonts/Nirmala.ttf"

if os.path.exists(font_path):
    pdfmetrics.registerFont(
        TTFont("Nirmala", font_path)
    )
    FONT_NAME = "Nirmala"
else:
    FONT_NAME = "Helvetica"


# ------------------------------------------------
# GENERATE PDF REPORT
# ------------------------------------------------

def generate_report(
    food_type,
    number_of_guests,
    event_type,
    quantity_of_food,
    storage_conditions,
    purchase_history,
    seasonality,
    preparation_method,
    geographical_location,
    pricing,
    result,
    suggested_quantity,
    reduction_percent,
    estimated_saving
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontName=FONT_NAME,
        alignment=TA_CENTER,
        fontSize=20,
        leading=24
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontName=FONT_NAME,
        fontSize=14,
        leading=18
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontName=FONT_NAME,
        fontSize=10,
        leading=14
    )

    italic_style = ParagraphStyle(
        "CustomItalic",
        parent=styles["Italic"],
        fontName=FONT_NAME,
        fontSize=9,
        leading=12
    )

    story = []

    # ------------------------------------------------
    # TITLE
    # ------------------------------------------------

    story.append(
        Paragraph(
            "Smart Food Waste Reduction Report",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    # ------------------------------------------------
    # FOOD DETAILS
    # ------------------------------------------------

    story.append(
        Paragraph(
            "Food Details",
            heading_style
        )
    )

    food_details = [
        ["Food Type", str(food_type)],
        ["Number of Guests", str(number_of_guests)],
        ["Event Type", str(event_type)],
        ["Quantity of Food", f"{quantity_of_food} units"],
        ["Storage Conditions", str(storage_conditions)],
        ["Purchase History", str(purchase_history)],
        ["Seasonality", str(seasonality)],
        ["Preparation Method", str(preparation_method)],
        ["Geographical Location", str(geographical_location)],
        ["Pricing", str(pricing)]
    ]

    table = Table(
        food_details,
        colWidths=[180, 300]
    )

    table.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # ------------------------------------------------
    # AI ANALYSIS
    # ------------------------------------------------

    story.append(
        Paragraph(
            "AI Agent Analysis",
            heading_style
        )
    )

    ai_analysis = [
        [
            "Predicted Food Waste",
            f"{result['predicted_waste']} units"
        ],
        [
            "Waste Risk",
            str(result["risk"])
        ],
        [
            "Current Quantity",
            f"{quantity_of_food} units"
        ],
        [
            "Suggested Quantity",
            f"{suggested_quantity:.1f} units"
        ],
        [
            "Possible Reduction",
            f"{reduction_percent}%"
        ],
        [
            "Estimated Cost Saving",
            f"Rs.{estimated_saving:.0f}"
        ]
    ]

    analysis_table = Table(
        ai_analysis,
        colWidths=[180, 300]
    )

    analysis_table.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(analysis_table)

    story.append(Spacer(1, 20))

    # ------------------------------------------------
    # AI RECOMMENDATIONS
    # ------------------------------------------------

    story.append(
        Paragraph(
            "AI Recommendations",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Recommendation:</b> {result['recommendation']}",
            body_style
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"<b>Smart Action:</b> {result['action']}",
            body_style
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"<b>Storage Tip:</b> {result['storage_tip']}",
            body_style
        )
    )

    story.append(Spacer(1, 20))

    # ------------------------------------------------
    # FOOTER
    # ------------------------------------------------

    story.append(
        Paragraph(
            "This report was generated by the Smart Food Waste Reduction Agent.",
            italic_style
        )
    )

    # ------------------------------------------------
    # BUILD PDF
    # ------------------------------------------------

    doc.build(story)

    buffer.seek(0)

    return buffer