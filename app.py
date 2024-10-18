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

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        profile = request.form.get('profile')
        skills = request.form.get('skills')
        education = request.form.get('education')
        projects = request.form.get('projects')
        training = request.form.get('training')

        # Basic validation
        if not name or not email:
            flash("Name and email are required fields.", "error")
            return redirect(url_for('index'))

        # Validate email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            flash("Invalid email format!", "error")
            return redirect(url_for('index'))

        # Store form data in session
        session['name'] = name
        session['email'] = email
        session['phone'] = phone
        session['profile'] = profile
        session['skills'] = skills
        session['education'] = education
        session['projects'] = projects
        session['training'] = training

        try:
            # Generate both PDF and Markdown files
            pdf_filename = generate_pdf(name, email, phone, profile, skills, education, projects, training)
            markdown_filename = generate_markdown(name, email, phone, profile, skills, education, projects, training)
        except Exception as e:
            flash(f"Failed to generate resume: {str(e)}", "error")
            return redirect(url_for('index'))

        # Clear the session after generating the resume
        session.clear()

        # Pass both PDF and Markdown filenames to the template
        return render_template('view_resume.html', pdf_filename=os.path.basename(pdf_filename), markdown_filename=os.path.basename(markdown_filename))

@app.route('/view_resume/<pdf_filename>/<markdown_filename>')
def view_resume(pdf_filename, markdown_filename):
    pdf_path = os.path.join('static', pdf_filename)
    markdown_path = os.path.join('static', markdown_filename)
    
    if not os.path.exists(pdf_path):
        flash("Resume not found!", "error")
        return redirect(url_for('index'))
    
    if not os.path.exists(markdown_path):
        flash("Markdown file not found!", "error")
        return redirect(url_for('index'))

    # Read and convert the Markdown file to HTML
    with open(markdown_path, 'r') as md_file:
        markdown_content = md_file.read()
        html_content = markdown.markdown(markdown_content)

    return render_template('view_resume.html', pdf_filename=pdf_filename, markdown_filename=markdown_filename, markdown_html=html_content)

@app.route('/download_resume/<filename>')
def download_resume(filename):
    file_path = os.path.join('static', filename)
    if not os.path.exists(file_path):
        flash("File not found!", "error")
        return redirect(url_for('index'))

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
