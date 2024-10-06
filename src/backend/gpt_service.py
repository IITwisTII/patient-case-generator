from openai import OpenAI
import json
import random
from config_loader import config_loader

client = OpenAI(api_key=config_loader.openai_api_key)


def load_diagnoses(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def generate_openai_response(client, system_prompt, user_prompts, model="gpt-3.5-turbo", max_tokens=1000, temperature=0.7):
    messages = [{"role": "system", "content": system_prompt}]
    
    for prompt in user_prompts:
        messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        content = response.choices[0].message.content
        
        # Attempt to load the content as JSON
        try:
            return json.loads(content)  # Try to parse as JSON for generate_patient_case
        except json.JSONDecodeError:
            return {"message": content}  # Return as plain text if JSON parsing fails for chat_with_patient
    except Exception as e:
        return {"error": str(e)}

# For generating patient case
def generate_patient_case(diagnoses):
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

# For generating SBAR report
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

# For chatting with the patient
# history is chat history up to that point in the current session
def chat_with_patient(user_input, patient_case, history):
    system_prompt = (
    f"You are a patient speaking to a medical doctor about your medical problems" 
    "and this is what has been said so far: '{history}'"
    )
    context = {
        "Situation": f"{patient_case['Symptoms']}.",
        "Background": f"{patient_case['Patient History']}.",
        "Assessment": f"{patient_case['Physical Examination Findings']}."
    }
    context_json = json.dumps(context)

    response = generate_openai_response(client, system_prompt, [context_json, user_input])
    
    return response

def evaluate_diagnosis(patient_case, chat_history):
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
    
    return generate_openai_response(client, system_prompt, [feedback_prompt],max_tokens=150 )

def assess_user_input(user_input):
    system_prompt = (
        "You are an AI that evaluates user input in a medical chat. "
        "Based on the following input, determine if the user is trying to give a diagnosis: "
    )

    user_prompt = f"User Input: '{user_input}'. Do you think the user is providing a diagnosis? Respond with 'yes' or 'no'."

    response = generate_openai_response(client, system_prompt, [user_prompt])
    return response.get("content", "no").strip().lower() == 'yes'  # Return True if the response is 'yes'

