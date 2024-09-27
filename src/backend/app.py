from flask import Flask, request, jsonify
from gpt_service import generate_patient_case, load_diagnoses
from flask_cors import CORS  # Import CORS to handle cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate-case', methods=['GET'])
def generate_case():
    # Call GPT model to generate patient case
    json_file_path = '../../media/icd10_diagnoses.json'  # Adjust the path as necessary
    diagnoses = load_diagnoses(json_file_path)
    
    # Generate a patient case
    patient_case = generate_patient_case(diagnoses)

    return jsonify({
        'case': patient_case
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
