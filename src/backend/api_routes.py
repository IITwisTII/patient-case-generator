from flask import Blueprint, jsonify, render_template, request, session
from gpt_service import generate_patient_case, load_diagnoses, generate_sbar_report, chat_with_patient

api_routes = Blueprint('api', __name__)

# Route to landing page
@api_routes.route('/')
def index_init():
    return render_template('index.html')

@api_routes.route('/chat')
def chat_init():
    return render_template('chat.html')

# Load diagnoses once to avoid repeated file access
json_file_path = '../../media/icd10_diagnoses.json'
diagnoses = load_diagnoses(json_file_path)

# Endpoint to generate a new patient case
@api_routes.route('/generate-case', methods=['GET'])
def generate_case():
    try:
        case = generate_patient_case(diagnoses)
        session['patient_case'] = case
        sbar = generate_sbar_report(case)
        return jsonify(sbar), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for chat messages related to the patient case
@api_routes.route('/chat/messages', methods=['POST'])
def chat_message():
    user_input = request.json.get('user_input')
    patient_case = session.get('patient_case')

    if not patient_case:
        return jsonify({"error": "No patient case found."}), 404

    # Retrieve chat history from session
    chat_history = session.get('chat_history', [])
    
    # Call the chat function with the user input, patient case, and current chat history
    response = chat_with_patient(user_input, patient_case, chat_history)
    
    # Update chat history with user input and AI response
    chat_history.append(f"User: {user_input}")
    chat_history.append(f"Patient: {response}")
    
    # Save updated chat history back into session
    session['chat_history'] = chat_history
    
    return jsonify({"response": response, "history": chat_history})
