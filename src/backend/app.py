from flask import Flask, request, jsonify
from gpt_service import generate_patient_case

app = Flask(__name__)

@app.route('/generate-case', methods=['POST'])
def generate_case():
    data = request.json
    prompt = data.get('prompt', '')

    # Call GPT model to generate patient case
    patient_case = generate_patient_case(prompt)

    return jsonify({
        'case': patient_case
    })

if __name__ == '__main__':
    app.run(debug=True)
