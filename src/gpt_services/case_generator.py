import json
import random
from .response_generator import generate_openai_response

def load_diagnoses(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        categorized_data = json.load(file)
    
    # Flatten the data into a list of dictionaries with 'category', 'code', and 'description'
    diagnoses = []
    for category, codes in categorized_data.items():
        for entry in codes:
            # Assuming each entry is a dictionary like {"code": "description"}
            for code, description in entry.items():
                diagnoses.append({
                    "category": category,
                    "code": code,
                    "description": description
                })
    
    return diagnoses

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
    return generate_openai_response(client, system_prompt, [user_prompt])

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

