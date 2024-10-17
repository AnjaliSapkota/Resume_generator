from flask import Flask, render_template, request, redirect, url_for, send_file
from util.pdfImage import generate_pdf  # Assuming this utility generates a PDF
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('resume_form.html')

@app.route('/generate', methods=['POST'])
def generate_resume():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        experience = request.form['experience']
        education = request.form['education']

        # Generate the resume PDF
        pdf_filename = generate_pdf(name, email, experience, education)  # Ensure this returns the filename

        # Redirect to a page that shows the user their generated resume
        return redirect(url_for('view_resume', pdf_filename=os.path.basename(pdf_filename)))  # Use basename for cleaner URLs

@app.route('/view_resume/<pdf_filename>')
def view_resume(pdf_filename):
    # Provide a link to view the PDF in the browser and also download it
    return f'''
    <h2>Your Resume is Ready!</h2>
    <iframe src="/static/{pdf_filename}" width="600" height="400"></iframe>  <!-- Embed the PDF -->
    <p><a href="/download_resume/{pdf_filename}">Download your Resume</a></p>  <!-- Provide a download link -->
    '''

@app.route('/download_resume/<pdf_filename>')
def download_resume(pdf_filename):
    # Serve the PDF for download
    return send_file(os.path.join('static', pdf_filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
