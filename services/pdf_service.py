from reportlab.platypus import SimpleDocTemplate,paragraph,Spacer

from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import streamlit as st

content = st.session_state["your_personalized_plan"] 


def create_pdf(content):
    buffer = BytesIO()
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(buffer)

    Story = []

    for line in content.split("\n"):
        Story.append(paragraph(line,styles["Normal"]))
        Story.append(Spacer(1,10))

        doc.build(Story)

        buffer.seek(0)
        return buffer