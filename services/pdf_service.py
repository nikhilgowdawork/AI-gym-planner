from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table

from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.lib.units import inch
import streamlit as st


def create_pdf(exercise_data, diet_data, supplements, tips):

    buffer = BytesIO()
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(buffer, pagesize=(8.5*inch, 11*inch))

    story = []

    # TITLE
    story.append(Paragraph("AI Personalized Fitness Plan", styles["Title"]))
    story.append(Spacer(1,20))



    # EXERCISE TABLE
    story.append(Paragraph("7-Day Exercise Plan", styles["Heading2"]))
    story.append(Spacer(1,10))

    exercise_table = [["Day","Exercise","Sets","Reps","Rest"]]

    for row in exercise_data:
        exercise_table.append([
        row["day"],
        row["exercise"],
        row["sets"],
        row["reps"],
        row["rest"]
    ])

    table = Table(exercise_table)
    story.append(table)


    # DIET TABLE
    story.append(Paragraph("7-Day Diet Plan", styles["Heading2"]))
    

    diet_table = [
    ["Day", "Breakfast", "Lunch", "Dinner", "Snacks", "Calories", "Protein"]
]

    for row in diet_data:
        diet_table.append([
        row["day"],
        row["breakfast"],
        row["lunch"],
        row["dinner"],
        row["snacks"],
        row["calories"],
        row["protein"]
    ])

    diet_table_obj = Table(diet_table)
    story.append(diet_table_obj)



    # SUPPLEMENTS
    story.append(Paragraph("Supplements (Optional)", styles["Heading2"]))
    story.append(Spacer(1,10))

    for s in supplements:
        story.append(Paragraph(f"• {s}", styles["Normal"]))

    story.append(Spacer(1,20))


    # HEALTH TIPS
    story.append(Paragraph("Practical Health Tips", styles["Heading2"]))
    story.append(Spacer(1,10))

    for t in tips:
        story.append(Paragraph(f"• {t}", styles["Normal"]))


    doc.build(story)

    buffer.seek(0)
    return buffer