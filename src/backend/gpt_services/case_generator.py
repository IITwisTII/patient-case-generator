import json
import random
from .response_generator import generate_openai_response

def load_diagnoses(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def generate_patient_case(client, diagnoses):
    diagnosis = random.choice(diagnoses)
    system_prompt = "You are a medical expert generating detailed medical cases."
    user_prompt = (
        f"Generate a detailed medical case for a patient diagnosed with '{diagnosis}'. "
        "Return the case in the following JSON format:\n"
        "{\n"
        "\"Patient History\": \"\",\n"
        "\"Symptoms\": \"\",\n"
        "\"Physical Examination Findings\": \"\",\n"
        "\"Lab Tests\": \"\",\n"
        "\"Radiology Results\": \"\",\n"
        "\"Diagnosis\": \"\",\n"
        "\"Treatment Plan\": \"\"\n"
        "}"
    )
    patient_case_generated = generate_openai_response(client, system_prompt, [user_prompt])
    print("Raw patient case Response:", patient_case_generated)  # Check raw response
    return patient_case_generated

def generate_sbar_report(patient_case):
    if isinstance(patient_case, dict):  # Ensure patient_case is a dictionary
        sbar = {
            "Situation": f"{patient_case['Symptoms']}.",
            "Background": f"{patient_case['Patient History']}.",
            "Assessment": f"{patient_case['Physical Examination Findings']}.",
            "Recommendation": f"{patient_case['Treatment Plan']}."
        }
        return sbar
    else:
        return {"error": "Invalid patient case format."}

