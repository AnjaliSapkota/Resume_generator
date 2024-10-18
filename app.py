import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from util.pdfImage import generate_pdf
from util.markdownResume import generate_markdown  # Import the markdown function
import os
import markdown  # Import the markdown library

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

@app.route('/')
def index():
    return render_template('resume_form.html')

@app.route('/step', methods=['POST'])
def step():
    # Collect data from the form
    session['name'] = request.form.get('name')
    session['email'] = request.form.get('email')
    session['phone'] = request.form.get('phone')
    session['profile'] = request.form.get('profile')
    session['skills'] = request.form.get('skills')
    session['education'] = request.form.get('education')
    session['projects'] = request.form.get('projects')
    session['training'] = request.form.get('training')

    # Redirect to the generate resume function
    return redirect(url_for('generate_resume'))

@app.route('/generate_resume')
def generate_resume():
    # Extract the session data to generate the resume
    name = session.get('name')
    email = session.get('email')
    phone = session.get('phone')
    profile = session.get('profile')
    skills = session.get('skills')
    education = session.get('education')
    projects = session.get('projects')
    training = session.get('training')

    # Basic validation
    if not name or not email:
        flash("Name and email are required fields.", "error")
        return redirect(url_for('index'))

    # Validate email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        flash("Invalid email format!", "error")
        return redirect(url_for('index'))

    try:
        # Generate both PDF and Markdown files
        pdf_filename = generate_pdf(name, email, phone, profile, skills, education, projects, training)
        markdown_filename = generate_markdown(name, email, phone, profile, skills, education, projects, training)
    except Exception as e:
        flash(f"Failed to generate resume: {str(e)}", "error")
        return redirect(url_for('index'))

    # Pass both PDF and Markdown filenames to the template
    return render_template('view_resume.html', pdf_filename=os.path.basename(pdf_filename), markdown_filename=os.path.basename(markdown_filename))

@app.route('/download_resume/<filename>')
def download_resume(filename):
    file_path = os.path.join('static', filename)
    if not os.path.exists(file_path):
        flash("File not found!", "error")
        return redirect(url_for('index'))

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
