import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from util.pdfImage import generate_pdf
import os

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
        projects = request.form.get('projects')
        education = request.form.get('education')
        profile = request.form.get('profile')
        skills = request.form.get('skills')
        phone = request.form.get('phone')
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
        session['projects'] = projects
        session['education'] = education
        session['profile'] = profile
        session['skills'] = skills
        session['phone'] = phone
        session['training'] = training

        try:
            pdf_filename = generate_pdf(name, email, projects, education, profile, skills, phone, training)
        except Exception as e:
            flash(f"Failed to generate PDF: {str(e)}", "error")
            return redirect(url_for('index'))

        return render_template('view_resume.html', pdf_filename=os.path.basename(pdf_filename))

@app.route('/view_resume/<pdf_filename>')
def view_resume(pdf_filename):
    pdf_path = os.path.join('static', pdf_filename)
    if not os.path.exists(pdf_path):
        flash("Resume not found!", "error")
        return redirect(url_for('index'))

    return send_file(pdf_path, as_attachment=False)

@app.route('/download_resume/<pdf_filename>')
def download_resume(pdf_filename):
    pdf_path = os.path.join('static', pdf_filename)
    if not os.path.exists(pdf_path):
        flash("File not found!", "error")
        return redirect(url_for('index'))

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
