from reportlab.platypus import SimpleDocTemplate,paragraph,Spacer,Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.lib.units import inch
import streamlit as st

content = st.session_state["your_personalized_plan"] 


def create_pdf(exercise_data, diet_data, supplements, tips):

    buffer = BytesIO()
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(buffer, pagesize=(8.5*inch, 11*inch))

    story = []

    # TITLE
    story.append(paragraph("AI Personalized Fitness Plan", styles["Title"]))
    story.append(Spacer(1,20))



    # EXERCISE TABLE
    story.append(paragraph("7-Day Exercise Plan", styles["Heading2"]))
    story.append(Spacer(1,10))

    exercise_table = Table(exercise_data)
    story.append(exercise_table)

    story.append(Spacer(1,20))


    # DIET TABLE
    story.append(paragraph("7-Day Diet Plan", styles["Heading2"]))
    story.append(Spacer(1,10))

    diet_table = Table(diet_data)
    story.append(diet_table)

    story.append(Spacer(1,20))


    # SUPPLEMENTS
    story.append(paragraph("Supplements (Optional)", styles["Heading2"]))
    story.append(Spacer(1,10))

    for s in supplements:
        story.append(paragraph(f"• {s}", styles["Normal"]))

    story.append(Spacer(1,20))


    # HEALTH TIPS
    story.append(paragraph("Practical Health Tips", styles["Heading2"]))
    story.append(Spacer(1,10))

    for t in tips:
        story.append(paragraph(f"• {t}", styles["Normal"]))


    doc.build(story)

    buffer.seek(0)
    return buffer