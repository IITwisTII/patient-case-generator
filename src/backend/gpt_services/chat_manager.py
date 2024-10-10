import json
from .response_generator import generate_openai_response

def chat_with_patient(client, user_input, patient_case, history):
    system_prompt = (
        "You are a patient speaking to a medical doctor about your medical problems "
        f"and this is what has been said so far: '{history}'"
        "Your role is to describe your symptoms, answer questions, and provide details about your condition as a real patient would."
    )
    context = {
        "Situation": f"{patient_case['Symptoms']}.",
        "Background": f"{patient_case['Patient History']}.",
        "Assessment": f"{patient_case['Physical Examination Findings']}."
    }
    context_json = json.dumps(context)

    response = generate_openai_response(client, system_prompt, [context_json, user_input])
    
    print("API Response:", response)
    return response
