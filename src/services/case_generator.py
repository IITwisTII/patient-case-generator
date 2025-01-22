import json
import random
from .response_generator import generate_openai_response
from utils.data_utils import load_diagnoses

def generate_patient_case(client, diagnoses):
    # Choose a random diagnosis from the loaded list
    json_file_path = '../media/final_icd_data.json'
    diagnoses = load_diagnoses(json_file_path)
    diagnosis = random.choice(diagnoses)

    category = diagnosis.get("category")
    code = diagnosis.get("code")
    description = diagnosis.get("description")

    if not category or not code or not description:
        raise ValueError("Missing data in diagnosis. Category, code, or description is None.")

    # Construct the system and user prompts
    system_prompt = "You are a medical expert generating detailed medical cases."
    user_prompt = (
        f"Generate a detailed medical case for a patient diagnosed with '{description}' (ICD-10 code: {code}, "
        f"category: {category}). "
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
    if isinstance(patient_case, dict): 
        sbar = {
            "Situation": f"{patient_case['Symptoms']}.",
            "Background": f"{patient_case['Patient History']}.",
            "Assessment": f"{patient_case['Physical Examination Findings']}.",
            "Recommendation": f"{patient_case['Treatment Plan']}."
        }
        return sbar
    else:
        return {"error": "Invalid patient case format."}

