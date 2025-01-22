from flask import Blueprint, jsonify, render_template, request, session
from services.openai_client import client
from services.case_generator import generate_patient_case, load_diagnoses, generate_sbar_report
from services.chat_manager import chat_with_patient
from services.evaluation import evaluate_diagnosis
from services.medical_test_results import perform_medical_test
from utils.commands import final_diagnosis_command, medical_test_command

api_routes = Blueprint('api', __name__)

json_file_path = '../media/final_icd_data.json'
diagnoses = load_diagnoses(json_file_path)

@api_routes.route('/generate-case', methods=['GET'])
def generate_case():
    try:
        # Clear previous session data
        session.pop('chat_history', None)
        session.pop('patient_case', None)

        case = generate_patient_case(client, diagnoses)
        session['patient_case'] = case
        sbar = generate_sbar_report(case)
        return jsonify(sbar), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_routes.route('/chat/messages', methods=['POST'])
def chat_message():
    user_input = request.json.get('user_input')
    if "patient_case" in session:
        patient_case = session.get('patient_case')
    else: 
        return jsonify({"error": "No patient case found."}), 404

    chat_history = session.get('chat_history', [])
    response = chat_with_patient(client, user_input, patient_case, chat_history).get('message')
    
    chat_history.append(f"User: {user_input}")
    chat_history.append(f"Patient: {response}")
    session['chat_history'] = chat_history
    
    first_element = user_input[0][0]
    if final_diagnosis_command(first_element):
        evaluation = evaluate_diagnosis(client, patient_case, chat_history)
        return jsonify({
            "history": chat_history,
            "chat_ended": True,
            "evaluation": evaluation
        }), 200
    elif medical_test_command(first_element):
        perform_medical_test(client, user_input, patient_case, chat_history)
        return
    
    return jsonify({"response": response, "history": chat_history})


@api_routes.route('/clear-chat-history', methods=['POST'])
def clear_chat_history():
    session.pop('chat_history', None)
    return jsonify({"message": "Chat history cleared."}), 200




