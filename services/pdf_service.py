from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table

from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


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

    exercise_table = [["Day","Exercise","Sets and reps","Rest"]]

    for row in exercise_data:
        exercise_table.append([

        row["day"],
        Paragraph(row["exercise"], styles["Normal"]),
        Paragraph(row["sets and reps"], styles["Normal"]),
        Paragraph(row["rest"], styles["Normal"])
    ])

    table = Table(
        exercise_table,colWidths=[60,170,90,130]

    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),

    ])) 
    story.append(table)


    # DIET TABLE
    story.append(Paragraph("7-Day Diet Plan", styles["Heading2"]))
    story.append(Spacer(1,10))

    def format_meal(text,styles):
        parts = text.split("(")
        main = parts[0]
        extra = "(" + parts[1] if len(parts) > 1 else ""

        bullet_text = f"""
        • {main.strip()} <br/>
        <font size = 8>{extra.strip()}</font>
        """
        return Paragraph(bullet_text, styles["Normal"])


    diet_table = [
    ["Day", "Breakfast", "Lunch", "Dinner", "Snacks", "Calories", "Protein"]
]

    for row in diet_data:
        diet_table.append([
        row["day"],
        format_meal(row["breakfast"],styles),
        format_meal(row["lunch"],styles),
        format_meal(row["dinner"],styles),
        format_meal(row["snacks"],styles),
        row["calories"],
        row["protein"],
    ])

    diet_table_obj = Table(
    diet_table,
    colWidths=[60,110,110,110,100,50,50]  # column sizes
)

    diet_table_obj.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("GRID",(0,0),(-1,-1),0.5,colors.grey),

    ("VALIGN",(0,0),(-1,-1),"TOP"),

    ("LEFTPADDING",(0,0),(-1,-1),6),
    ("RIGHTPADDING",(0,0),(-1,-1),6),
    ("TOPPADDING",(0,0),(-1,-1),6),
    ("BOTTOMPADDING",(0,0),(-1,-1),6)
    ]))

    story.append(diet_table_obj)
    story.append(Spacer(1,20))
    

    


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