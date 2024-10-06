import json
from .response_generator import generate_openai_response

def evaluate_diagnosis(client, patient_case, chat_history):
    system_prompt = (
        "You are a medical expert evaluating a doctor's diagnosis and decision-making process. "
        "Provide feedback based on the tests they ordered and the diagnosis they made."
    )
    
    feedback_prompt = (
        f"Patient Case: {json.dumps(patient_case)}\n"
        f"Doctor's Diagnosis: {chat_history}\n"
        "Evaluate the doctor's reasoning and provide feedback. Score them from 0 to 10 based on accuracy "
        "of diagnosis and quality of decision-making."
    )
    
    return generate_openai_response(client, system_prompt, [feedback_prompt], max_tokens=150)

def assess_user_input(client, user_input):
    system_prompt = (
        "You are an AI that evaluates user input in a medical chat. "
        "Based on the following input, determine if the user is trying to give a diagnosis: "
    )

    user_prompt = f"User Input: '{user_input}'. Do you think the user is providing a diagnosis? Respond with 'yes' or 'no'."

    response = generate_openai_response(client, system_prompt, [user_prompt])
    return response.get("content", "no").strip().lower() == 'yes'  # Return True if the response is 'yes'
