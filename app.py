import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import utils
import markdown2
from markdownResume import generate_markdown

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

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

def draw_wrapped_text(c, text, x, y, width, font_name="Helvetica", font_size=12, leading=15):
    """Draws text wrapped within a certain width and returns the final y position after the text is drawn."""
    c.setFont(font_name, font_size)
    text_object = c.beginText(x, y)
    text_object.setLeading(leading)
    lines = utils.simpleSplit(text, font_name, font_size, width)

    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)
    
    return y - len(lines) * leading  # Return the final y position after text is drawn

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

    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, y_position, name)
    y_position -= 30

    c.setFont("Helvetica", 12)
    c.drawString(margin, y_position, f"Email: {email}")
    y_position -= 20
    if phone:
        c.drawString(margin, y_position, f"Phone: {phone}")
        y_position -= 30
    else:
        y_position -= 20

    c.line(margin, y_position, width - margin, y_position)
    y_position -= 30

    profile_width = width - 2 * margin  # Calculate available width for profile text

    if profile:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Profile Summary:")
        y_position -= 20
        y_position = draw_wrapped_text(c, profile, margin, y_position, profile_width)
        y_position -= 10

    if skills:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Skills:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        skills_list = skills.splitlines()
        for skill in skills_list:
            c.drawString(margin, y_position, f"- {skill.strip()}")
            y_position -= 15
        y_position -= 10

    if education:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Education:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        for edu in education.splitlines():
            y_position = draw_wrapped_text(c, edu.strip(), margin, y_position, width - 2 * margin)
        y_position -= 10

    if projects:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Projects:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        for proj in projects.splitlines():
            y_position = draw_wrapped_text(c, proj.strip(), margin, y_position, width - 2 * margin)
        y_position -= 10

    if training:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y_position, "Training & Certifications:")
        y_position -= 20
        c.setFont("Helvetica", 12)
        for cert in training.splitlines():
            y_position = draw_wrapped_text(c, f"- {cert.strip()}", margin, y_position, width - 2 * margin)

    c.save()

    # Send the PDF as a downloadable file
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
