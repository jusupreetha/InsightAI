import os
import tempfile
from io import BytesIO
from datetime import datetime
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
)


def create_report(
    title,
    subtitle,
    dataset_name,
    executive_summary=None,
    summary=None,
    charts=None,
):    
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    heading_style.alignment = TA_CENTER

    story = []

    
    story.append(Spacer(1, 20))
    

    if subtitle:
        story.append(
    Paragraph(
        "<font size=26><b>InsightAI</b></font>",
        title_style,
    )
)

        story.append(Spacer(1, 8))

        story.append(
    Paragraph(
        "<font size=13 color='grey'>AI-Powered Data Analytics Platform</font>",
        heading_style,
    )
)

        story.append(Spacer(1, 35))

        story.append(
    Paragraph(
        f"<font size=22><b>{title}</b></font>",
        title_style,
    )
)

        story.append(Spacer(1, 20))
        story.append(PageBreak())

    story.append(
        Paragraph(
            f"<b>Dataset:</b> {dataset_name}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%d %b %Y %I:%M %p')}",
            styles["Normal"],
        )
    )

    story.append(Spacer(1, 40))

    # Executive Summary
    if executive_summary:

        story.append(Spacer(1, 30))

        story.append(
            Paragraph(
            "Executive Summary",
            styles["Heading1"],
        )
    )

        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
            executive_summary.replace("\n", "<br/>"),
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 40))
    
          
    # KPI Overview
    if summary:

        story.append(Spacer(1, 25))

        story.append(
        Paragraph(
            "Dataset Overview",
            styles["Heading1"],
        )
    )

        story.append(Spacer(1, 10))

        kpis = [
        ("Rows", summary["rows"]),
        ("Columns", summary["columns"]),
        ("Missing Values", summary["missing_values"]),
        ("Duplicates", summary["duplicates"]),
    ]

        for label, value in kpis:
            story.append(
            Paragraph(
                f"<b>{label}:</b> {value}",
                styles["BodyText"],
            )
        )   
        
    # Charts
    if charts:

        story.append(Spacer(1, 25))

        story.append(
        Paragraph(
            "Visualizations",
            styles["Heading1"],
        )
    )

        story.append(Spacer(1, 12))

        temp_files = []
        for card in charts:

            fig = card.get("figure")

            if fig is None:
                continue

            with tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False,
    ) as tmp:

                temp_path = tmp.name

            fig.write_image(temp_path, scale=2)
            temp_files.append(temp_path)

            story.append(
        Paragraph(
            card.get("title", "Chart"),
            styles["Heading2"],
        )
    )

            story.append(
        Image(
            temp_path,
            width=420,
            height=240,
        )
    )

            story.append(Spacer(1, 20))

            #os.remove(temp_path)
    story.append(
        Paragraph(
        "<b>Generated with InsightAI</b>",
        heading_style,
    )
)
    #for path in temp_files:
        #if os.path.exists(path):
             #os.remove(path)
    
    doc.build(story)
    buffer.seek(0)

    return buffer