# src/pdf/export_pdf.py

import sys
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

# -------------------- PATH SETUP --------------------

BASE_DIR = Path(__file__).resolve().parents[2]  
SUMMARY_DIR = BASE_DIR / "output" / "summary"
ACTIONS_DIR = BASE_DIR / "output" / "action_items"
OUTPUT_DIR = BASE_DIR / "output" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------- Load Text --------------------

def load_text(path):
    return path.read_text(encoding="utf-8") if path.exists() else "[Not Found]"

# -------------------- PDF Builder --------------------

def export_to_pdf(audio_name):
    summary_path = SUMMARY_DIR / f"{audio_name}_summary.txt"
    actions_path = ACTIONS_DIR / f"{audio_name}_action_items.txt"
    output_path = OUTPUT_DIR / f"{audio_name}_report.pdf"

    summary = load_text(summary_path)
    actions = load_text(actions_path)

    doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        name='TitleCenter', parent=styles['Title'],
        alignment=TA_CENTER, fontSize=18, spaceAfter=14
    )
    timestamp_style = ParagraphStyle(
        name='Timestamp', parent=styles['Normal'],
        fontSize=9, textColor=colors.grey, alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        name='SectionHeading', parent=styles['Heading2'],
        textColor=colors.HexColor("#2A6592"), spaceBefore=12, spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        name='BulletPoint', parent=styles['Normal'],
        leftIndent=18, bulletIndent=6, spaceBefore=4, spaceAfter=4
    )

    elements = []

    # Title
    elements.append(Paragraph(f"🗂️ Meeting Report: <b>{audio_name}</b>", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", timestamp_style))
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(HRFlowable(color=colors.grey, thickness=0.5))
    elements.append(Spacer(1, 0.6 * cm))

    # Summary
    elements.append(Paragraph("📝 Summary", heading_style))
    for line in summary.strip().splitlines():
        if line.strip():
            elements.append(Paragraph(line.strip(), styles['Normal']))
    elements.append(Spacer(1, 0.6 * cm))
    elements.append(HRFlowable(color=colors.grey, thickness=0.5))
    elements.append(Spacer(1, 0.6 * cm))

    # Action Items
    elements.append(Paragraph("📌 Action Items", heading_style))
    bullet_items = []
    for line in actions.strip().splitlines():
        if line.strip():
            bullet_items.append(ListItem(Paragraph(line.strip(), bullet_style)))

    if bullet_items:
        elements.append(ListFlowable(bullet_items, bulletType='bullet', start='circle', leftIndent=12))
    else:
        elements.append(Paragraph("No action items found.", styles['Normal']))

    doc.build(elements)
    print(f"✅ Styled PDF saved to: {output_path}")

# -------------------- CLI --------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python export_pdf.py <audio_name>")
    else:
        export_to_pdf(sys.argv[1])
