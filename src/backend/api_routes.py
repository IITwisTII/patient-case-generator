from flask import Blueprint, jsonify, render_template, request, session
from gpt_service import generate_patient_case, load_diagnoses, generate_sbar_report, chat_with_patient

api_routes = Blueprint('api', __name__)

# Route to serve the HTML page
@api_routes.route('/')
def index_init():
    return render_template('index.html')

@api_routes.route('/chat')
def chat_init():
    return render_template('chat.html')

# In-memory store for patient cases
patient_cases = {}

# When generating a patient case
@api_routes.route('/generate-case', methods=['GET'])
def generate_case():
    # Call GPT model to generate patient case
    json_file_path = '../../media/icd10_diagnoses.json'  # Adjust the path as necessary
    diagnoses = load_diagnoses(json_file_path)
    
    case = generate_patient_case(diagnoses)
    session['patient_case'] = case 
    sbar = generate_sbar_report(case)

    return jsonify(sbar)

@api_routes.route('/chat/message', methods=['POST'])
def chat_message():
    user_input = request.json.get('user_input')
    patient_case = session.get('patient_case')  # Retrieve the patient case from session

    if patient_case:
        response = chat_with_patient(user_input, patient_case)
    else:
        response = {"response": "No patient case found."}

    return jsonify(response)
