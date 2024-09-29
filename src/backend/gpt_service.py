from openai import OpenAI
import os
import json
import random
import importlib.util

if os.name == "nt": 
    config_file_path = 'c:/config.py'
    spec = importlib.util.spec_from_file_location("config", config_file_path)
elif os.name == "posix":
    config_file_path = '/home/alikashash/config.py'  # Linux path
    spec = importlib.util.spec_from_file_location("config", config_file_path)
    
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

# Set your OpenAI API key
client = OpenAI(api_key=config.OPENAI_API_KEY)

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
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return {"error": str(e)}

# Example usage with different prompts:

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
    system_prompt = "You are a medical expert generating SBAR reports based on patient cases."
    user_prompt = json.dumps(patient_case)  # Convert patient case to JSON format
    return generate_openai_response(client, system_prompt, [user_prompt], max_tokens=500)

# For chatting with the patient
def chat_with_patient(user_input, patient_case):
    system_prompt = "You are a patient speaking to a medical doctor about your medical problems."
    context = {
        "Situation": f"{patient_case['Symptoms']}.",
        "Background": f"{patient_case['Patient History']}.",
        "Assessment": f"{patient_case['Physical Examination Findings']}."
    }
    context_json = json.dumps(context)
    
    return generate_openai_response(client, system_prompt, [context_json, user_input], max_tokens=150)
