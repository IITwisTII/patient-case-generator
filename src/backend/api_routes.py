from flask import Blueprint, jsonify, render_template
from gpt_service import generate_patient_case, load_diagnoses

api_routes = Blueprint('api', __name__)

# Route to serve the HTML page
@api_routes.route('/')
def index():
    return render_template('index.html')

# When generating a patient case
@api_routes.route('/generate-case', methods=['GET'])
def generate_case():
    # Call GPT model to generate patient case
    json_file_path = 'media\icd10_diagnoses.json'  # Adjust the path as necessary
    diagnoses = load_diagnoses(json_file_path)
    
    # Generate a patient case
    patient_case = generate_patient_case(diagnoses)

    return jsonify({
        'case': patient_case
    })
