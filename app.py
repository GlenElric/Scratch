from flask import Flask, render_template, request, redirect, url_for, send_file
import requests
from weasyprint import HTML
import os

app = Flask(__name__)

SCRATCH_API_URL = "https://api.scratch.mit.edu/projects/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project', methods=['POST'])
def project():
    project_id = request.form.get('project_id')
    if not project_id:
        return redirect(url_for('index'))

    project_data = get_scratch_project(project_id)
    if project_data:
        return render_template('project.html', project=project_data)
    else:
        return "Project not found or an error occurred."

def get_scratch_project(project_id):
    try:
        response = requests.get(f"{SCRATCH_API_URL}{project_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching Scratch project: {e}")
        return None

@app.route('/generate_pdf/<project_id>')
def generate_pdf(project_id):
    project_data = get_scratch_project(project_id)
    if not project_data:
        return "Error generating PDF: Project not found."
    
    # Render project data to HTML for PDF generation
    rendered_html = render_template('project_pdf.html', project=project_data)
    pdf = HTML(string=rendered_html).write_pdf()

    pdf_path = os.path.join('static', f'{project_id}.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf)
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)