from flask import Flask, jsonify, request, send_file
from util.pdfImage import generate_pdf  # Make sure this utility generates a PDF
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Resume Builder API!"})

@app.route('/generate_resume', methods=['POST'])
def generate_resume_api():
    # API endpoint to generate a resume
    if request.method == 'POST':
        # Get form data from JSON
        data = request.get_json()
        
        # Extracting data with error handling
        try:
            name = data['name']
            email = data['email']
            experience = data['experience']
            education = data['education']
        except KeyError as e:
            return jsonify({"error": f"Missing key: {e}"}), 400

        # Generate the resume PDF
        pdf_filename = generate_pdf(name, email, experience, education)  # Ensure this returns the filename
        
        # Respond with the PDF download link
        return jsonify({
            "message": "Resume generated successfully!",
            "download_link": f"/download_resume/{os.path.basename(pdf_filename)}"
        })

@app.route('/download_resume/<pdf_filename>')
def download_resume(pdf_filename):
    # Serve the PDF for download
    return send_file(os.path.join('static', pdf_filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
