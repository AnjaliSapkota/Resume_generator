import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import markdown2
from markdownResume import generate_markdown

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

def wrap_text(text, max_width, c, margin, y_position):
    """Helper function to wrap text within a specified width."""
    words = text.split(' ')
    lines = []
    line = ""

    for word in words:
        if c.stringWidth(line + word + " ") <= max_width:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    if line:
        lines.append(line)

    for wrapped_line in lines:
        c.drawString(margin, y_position, wrapped_line)
        y_position -= 15  # Move to next line height

    return y_position

@app.route('/')
def index():
    return render_template('resume_form.html')

@app.route('/step', methods=['POST'])
def step():
    session['name'] = request.form.get('name')
    session['email'] = request.form.get('email')
    session['phone'] = request.form.get('phone')
    session['profile'] = request.form.get('profile')
    session['skills'] = request.form.get('skills')
    session['education'] = request.form.get('education')
    session['projects'] = request.form.get('projects')
    session['training'] = request.form.get('training')

    return redirect(url_for('generate_resume'))

@app.route('/generate_resume')
def generate_resume():
    name = session.get('name')
    email = session.get('email')
    
    if not name or not email:
        flash("Name and email are required fields.", "error")
        return redirect(url_for('index'))

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        flash("Invalid email format!", "error")
        return redirect(url_for('index'))

    try:
        markdown_filename = generate_markdown(
            name,
            email,
            session.get('phone'),
            session.get('profile'),
            session.get('skills'),
            session.get('education'),
            session.get('projects'),
            session.get('training')
        )

        with open(markdown_filename, 'r') as md_file:
            markdown_content = md_file.read()
            html_content = markdown2.markdown(markdown_content)

        return render_template('view_resume.html', html_content=html_content)

    except Exception as e:
        flash(f"Failed to generate resume: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/download_pdf')
def download_pdf():
    name = session.get('name')
    email = session.get('email')
    phone = session.get('phone')
    profile = session.get('profile')
    skills = session.get('skills')
    education = session.get('education')
    projects = session.get('projects')
    training = session.get('training')

    pdf_filename = f"{name.replace(' ', '_')}_resume.pdf"
    pdf_path = os.path.join('static', pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    margin = 50  
    y_position = height - margin  

    # Name
    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, y_position, name)
    y_position -= 30

    # Email and phone
    c.setFont("Helvetica", 12)
    c.drawString(margin, y_position, f"Email: {email}")
    y_position -= 20
    if phone:
        c.drawString(margin, y_position, f"Phone: {phone}")
        y_position -= 30
    else:
        y_position -= 20

    # Line separator
    c.line(margin, y_position, width - margin, y_position)
    y_position -= 30

    # Profile Summary
    if profile:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Profile Summary:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        # Wrap text for profile summary
        y_position = wrap_text(profile, width - 2 * margin, c, margin, y_position)
        y_position -= 10

    # Skills
    if skills:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Skills:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        # Wrap text for skills
        y_position = wrap_text(skills, width - 2 * margin, c, margin, y_position)
        y_position -= 10

    # Education
    if education:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Education:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        # Wrap text for education
        y_position = wrap_text(education, width - 2 * margin, c, margin, y_position)
        y_position -= 10

    # Projects
    if projects:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Projects:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        # Wrap text for projects
        y_position = wrap_text(projects, width - 2 * margin, c, margin, y_position)
        y_position -= 10

    # Training & Certifications
    if training:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Training & Certifications:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        # Wrap text for training
        y_position = wrap_text(training, width - 2 * margin, c, margin, y_position)

    c.save()

    # Send the PDF as a downloadable file
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
