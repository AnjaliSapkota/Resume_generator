from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime

def generate_pdf(name, email, phone, projects, education, profile, skills, training):
    # Define file path for the PDF
    pdf_filename = f"static/resume_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    
    # Set up the canvas for the PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Font settings
    title_font = "Helvetica-Bold"
    text_font = "Helvetica"

    # --- Name on Top Centered ---
    c.setFont(title_font, 24)
    text_width = c.stringWidth(name, title_font, 24)
    c.drawString((width - text_width) / 2, 750, name)

    # --- Email and Phone Below Name (Centered) ---
    c.setFont(text_font, 12)
    contact_info = f"{email}   |   {phone}"
    contact_width = c.stringWidth(contact_info, text_font, 12)
    c.drawString((width - contact_width) / 2, 735, contact_info)

    # --- Horizontal Line under Contact Info ---
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(50, 710, width - 50, 710)

    # Define positions for the two columns
    column_1_x = 50
    column_2_x = 320
    vertical_line_x = 300
    current_y = 690

    # --- Add Vertical Line between the Columns (not touching horizontal line) ---
    c.line(vertical_line_x, 690, vertical_line_x, 100)  # Adjusted to not touch the horizontal line

    # --- Column 1: Profile and Skills ---
    # Section: Profile (Underlined)
    c.setFont(title_font, 16)
    c.drawString(column_1_x, current_y, "PROFILE")
    c.line(column_1_x, current_y - 2, column_1_x + 60, current_y - 2)  # Underline
    current_y -= 20
    c.setFont(text_font, 12)
    profile_text = c.beginText(column_1_x, current_y)
    for line in profile.split('\n'):
        profile_text.textLine(line)
    c.drawText(profile_text)
    current_y -= 100  # Adjust space

    # Section: Skills (Underlined)
    c.setFont(title_font, 16)
    c.drawString(column_1_x, current_y, "SKILLS")
    c.line(column_1_x, current_y - 2, column_1_x + 60, current_y - 2)  # Underline
    current_y -= 20
    skills_text = c.beginText(column_1_x, current_y)
    for skill in skills.split(','):
        skills_text.textLine(f"- {skill.strip()}")
    c.drawText(skills_text)
    current_y -= 100

    # --- Column 2: Education, Certifications, and Professional Experience ---
    current_y = 690  # Reset Y for second column
    # Section: Education (Underlined)
    c.setFont(title_font, 16)
    c.drawString(column_2_x, current_y, "EDUCATION")
    c.line(column_2_x, current_y - 2, column_2_x + 100, current_y - 2)  # Underline
    current_y -= 20
    c.setFont(text_font, 12)
    education_text = c.beginText(column_2_x, current_y)
    for line in education.split('\n'):
        education_text.textLine(line)
    c.drawText(education_text)
    current_y -= 100  # Adjust space

    # Section: Certifications (Underlined)
    c.setFont(title_font, 16)
    c.drawString(column_2_x, current_y, "CERTIFICATIONS")
    c.line(column_2_x, current_y - 2, column_2_x + 130, current_y - 2)  # Underline
    current_y -= 20
    certifications_text = c.beginText(column_2_x, current_y)
    for line in training.split('\n'):
        certifications_text.textLine(line)
    c.drawText(certifications_text)
    current_y -= 100

    # Section: Professional Experience (Underlined)
    c.setFont(title_font, 16)
    c.drawString(column_2_x, current_y, "PROFESSIONAL EXPERIENCE")
    c.line(column_2_x, current_y - 2, column_2_x + 180, current_y - 2)  # Underline
    current_y -= 20
    experience_text = c.beginText(column_2_x, current_y)
    for project in projects.split('\n'):
        experience_text.textLine(project)
    c.drawText(experience_text)

    # Footer section
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    c.drawString(50, 50, "Generated with ReportLab - Python PDF Library")

    # Save the PDF
    c.showPage()
    c.save()

    return pdf_filename
