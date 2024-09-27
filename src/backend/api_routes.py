from flask import Blueprint, jsonify, render_template
from gpt_service import generate_patient_case, load_diagnoses, generate_sbar_report

api_routes = Blueprint('api', __name__)

# Route to serve the HTML page
@api_routes.route('/')
def index_init():
    return render_template('index.html')

@api_routes.route('/chat')
def chat_init():
    return render_template('chat.html')

# When generating a patient case
@api_routes.route('/generate-case', methods=['GET'])
def generate_case():
    # Call GPT model to generate patient case
    json_file_path = '../../media/icd10_diagnoses.json'  # Adjust the path as necessary
    diagnoses = load_diagnoses(json_file_path)
    
    case = generate_patient_case(diagnoses)
    
    sbar = generate_sbar_report(case)

    return jsonify(sbar)
