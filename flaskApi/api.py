from flask import Flask, jsonify, request, send_file, session
from util.pdfImage import generate_pdf  # Utility to generate a PDF
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')  # Use environment variable for production

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Resume Builder API!"})

@app.route('/generate_resume', methods=['POST'])
def generate_resume_api():
    # API endpoint to generate a resume
    if request.method == 'POST':
        data = request.get_json()

        # Required fields and validation
        required_fields = ['name', 'email', 'projects', 'education', 'profile', 'skills', 'phone', 'training']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        name = data.get('name')
        email = data.get('email')
        projects = data.get('projects')
        education = data.get('education')
        profile = data.get('profile')
        skills = data.get('skills')
        phone = data.get('phone')
        training = data.get('training')

        # Improved Email validation using regex
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email format"}), 400

        # Store form data in session
        session['name'] = name
        session['email'] = email
        session['projects'] = projects
        session['education'] = education
        session['profile'] = profile
        session['skills'] = skills
        session['phone'] = phone
        session['training'] = training

        # Generate the resume PDF
        try:
            pdf_filename = generate_pdf(name, email, projects, education, profile, skills, phone, training)
        except Exception as e:
            return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

        # Respond with the PDF download link
        return jsonify({
            "message": "Resume generated successfully!",
            "download_link": f"/download_resume/{os.path.basename(pdf_filename)}"
        })

@app.route('/download_resume/<pdf_filename>')
def download_resume(pdf_filename):
    # Serve the PDF for download
    pdf_path = os.path.join('static', pdf_filename)
    if not os.path.exists(pdf_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
