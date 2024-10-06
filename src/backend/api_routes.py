from flask import Blueprint, jsonify, render_template, request, session
from gpt_services.openai_client import client
from gpt_services.case_generator import generate_patient_case, load_diagnoses, generate_sbar_report
from gpt_services.chat_manager import chat_with_patient
from gpt_services.evaluation import evaluate_diagnosis, assess_user_input

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

# Generate Case
@api_routes.route('/generate-case', methods=['GET'])
def generate_case():
    try:
        case = generate_patient_case(client, diagnoses)
        session['patient_case'] = case
        sbar = generate_sbar_report(case)
        return jsonify(sbar), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Chat
@api_routes.route('/chat/messages', methods=['POST'])
def chat_message():
    user_input = request.json.get('user_input')
    patient_case = session.get('patient_case')

    if not patient_case:
        return jsonify({"error": "No patient case found."}), 404

    chat_history = session.get('chat_history', [])
    
    response = chat_with_patient(client, user_input, patient_case, chat_history).get('message')
    
    chat_history.append(f"User: {user_input}")
    chat_history.append(f"Patient: {response}")
    
    session['chat_history'] = chat_history
    
    if assess_user_input(client, user_input):  # Check if the user seems to give a diagnosis
        evaluation = evaluate_diagnosis(client, patient_case, chat_history)
        return jsonify({
            "response": response,
            "history": chat_history,
            "chat_ended": True,  # Indicate that the chat has ended
            "evaluation": evaluation
        }), 200
    
    return jsonify({"response": response, "history": chat_history})


@api_routes.route('/clear-chat-history', methods=['POST'])
def clear_chat_history():
    session.pop('chat_history', None)  # Remove chat_history from session
    return jsonify({"message": "Chat history cleared."}), 200