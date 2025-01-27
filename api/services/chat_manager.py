import json
from .response_generator import generate_openai_response

def chat_with_patient(client, user_input, patient_case, history):
    system_prompt = (
        "You are a patient speaking to a medical doctor about your medical issues. "
        "You are supposed to describe your symptoms, answer questions about your condition, "
        "and provide any other details as a real patient would. "
        "You will respond in the first person as if you are the patient, not the doctor."
        "\nThe context of the conversation is as follows:\n"
        f"History: {history}\n"
        "Now, the user is asking about your symptoms or condition. Please respond as the patient."
    )

    context = {
        "Situation": f"{patient_case['Symptoms']}",
        "Background": f"{patient_case['Patient History']}",
        "Assessment": f"{patient_case['Physical Examination Findings']}"
    }
    context_json = json.dumps(context)
    
    response = generate_openai_response(client, system_prompt, [context_json, user_input])

    print("API Response:", response)
    return response
