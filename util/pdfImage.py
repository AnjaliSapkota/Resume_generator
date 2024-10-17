from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(name, email, experience, education):
    file_path = f"static/resume_{name}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    
    # Title
    c.setFont("Helvetica", 20)
    c.drawString(100, 750, f"Resume: {name}")

    # Email
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Email: {email}")

    # Experience
    c.drawString(100, 690, "Experience:")
    text = c.beginText(100, 670)
    text.setFont("Helvetica", 12)
    for line in experience.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Education
    c.drawString(100, 600, "Education:")
    text = c.beginText(100, 580)
    for line in education.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Save PDF
    c.showPage()
    c.save()

    return file_path
