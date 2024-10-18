from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime

def generate_pdf(name, email, phone, profile, skills, education, projects, training):
    pdf_filename = f"static/resume_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    title_font = "Helvetica-Bold"
    text_font = "Helvetica"

    # Name 
    c.setFont(title_font, 24)
    text_width = c.stringWidth(name, title_font, 24)
    c.drawString((width - text_width) / 2, 750, name)

    # Email and Phone
    c.setFont(text_font, 12)
    contact_info = f"{email}   |   {phone}"
    contact_width = c.stringWidth(contact_info, text_font, 12)
    c.drawString((width - contact_width) / 2, 735, contact_info)

    # Horizontal Line
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(50, 710, width - 50, 710)

    # Profile Summary 
    c.setFont(title_font, 18)
    c.drawString(50, 680, "Profile Summary:")
    c.setFont(text_font, 12)
    c.drawString(50, 660, profile)

    # Skills 
    c.setFont(title_font, 18)
    c.drawString(50, 620, "Skills:")
    c.setFont(text_font, 12)
    skills_list = skills.splitlines()
    y_position = 600
    for skill in skills_list:
        c.drawString(50, y_position, f"- {skill}")
        y_position -= 15

    # Education
    c.setFont(title_font, 18)
    c.drawString(50, y_position - 20, "Education:")
    c.setFont(text_font, 12)
    education_list = education.splitlines()
    y_position -= 40
    for edu in education_list:
        c.drawString(50, y_position, f"- {edu}")
        y_position -= 15

    # Projects
    c.setFont(title_font, 18)
    c.drawString(50, y_position - 20, "Projects:")
    c.setFont(text_font, 12)
    projects_list = projects.splitlines()
    y_position -= 40
    for project in projects_list:
        c.drawString(50, y_position, f"- {project}")
        y_position -= 15

    # Training 
    c.setFont(title_font, 18)
    c.drawString(50, y_position - 20, "Training:")
    c.setFont(text_font, 12)
    training_list = training.splitlines()
    y_position -= 40
    for train in training_list:
        c.drawString(50, y_position, f"- {train}")
        y_position -= 15

    c.save()

    return pdf_filename
