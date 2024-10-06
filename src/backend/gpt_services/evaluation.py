import json
from .response_generator import generate_openai_response

def evaluate_diagnosis(client, patient_case, chat_history):
    system_prompt = (
        "You are a medical expert evaluating a doctor's diagnosis and decision-making process. "
        "Provide feedback based on the tests they ordered and the diagnosis they made."
        "You will be provided with the Patients Case."
        "You will be provided with the chat_history and in it you will have to understand what the Doctor's Diagnosis (including deduction and tests taken) is."
    )
    
    feedback_prompt = (
        f"Patient Case: {json.dumps(patient_case)}\n"
        f"Doctor's Diagnosis: {chat_history}\n"
        "Evaluate the doctor's reasoning and provide feedback. Score them from 0 to 10 based on accuracy "
        "of diagnosis and quality of decision-making."
    )
    feedback_prompt = json.dumps(feedback_prompt)
    
    return generate_openai_response(client, system_prompt, [feedback_prompt], max_tokens=150)