from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

def generate_pdf(name, email, projects, education, profile, skills, phone, training):
    try:
        # Generate unique filename with timestamp
        pdf_filename = f"static/resume_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        # Title (Name)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, 750, name)

        # Contact Information (Email and Phone)
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"Email: {email} | Phone: {phone}")

        # Horizontal Line
        c.setStrokeColor(colors.grey)
        c.setLineWidth(1)
        c.line(100, 715, 500, 715)

        # Profile Section
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 690, "PROFILE")
        c.setFont("Helvetica", 12)
        profile_text = c.beginText(100, 670)
        for line in profile.split('\n'):
            profile_text.textLine(line)
        c.drawText(profile_text)

        # Skills Section
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 620, "SKILLS")
        c.setFont("Helvetica", 12)
        skills_text = c.beginText(100, 600)
        for skill in skills.split(','):
            skills_text.textLine(f"- {skill.strip()}")
        c.drawText(skills_text)

        # Projects Section
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 550, "PROJECTS")
        c.setFont("Helvetica", 12)
        projects_text = c.beginText(100, 530)
        for project in projects.split('\n'):
            projects_text.textLine(project)
        c.drawText(projects_text)

        # Education Section
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 450, "EDUCATION")
        c.setFont("Helvetica", 12)
        education_text = c.beginText(100, 430)
        for line in education.split('\n'):
            education_text.textLine(line)
        c.drawText(education_text)

        # Training Section
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 350, "TRAINING & CERTIFICATIONS")
        c.setFont("Helvetica", 12)
        training_text = c.beginText(100, 330)
        for line in training.split('\n'):
            training_text.textLine(line)
        c.drawText(training_text)

        # Footer Section
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(colors.grey)
        c.drawString(100, 100, "Generated with ReportLab - Python PDF Library")

        # Save PDF
        c.showPage()
        c.save()

        return pdf_filename
    except Exception as e:
        raise Exception(f"Error in PDF generation: {str(e)}")
