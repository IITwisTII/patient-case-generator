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

def generate_patient_case(diagnoses):

    # Pick a random diagnosis
    diagnosis = random.choice(diagnoses)

    messages = [
        {"role": "system", "content": "You are a medical expert generating detailed medical cases."},
        {
            "role": "user",
            "content": (f"Generate a detailed medical case for a patient diagnosed with '{diagnosis}'. "
                        "Return the case in the following JSON format:\n"
                        "{\n"
                        "\"Patient History\": \"\",\n"
                        "\"Symptoms\": \"\",\n"
                        "\"Physical Examination Findings\": \"\",\n"
                        "\"Lab Tests\": \"\",\n"
                        "\"Radiology Results\": \"\",\n"
                        "\"Diagnosis\": \"\",\n"
                        "\"Treatment Plan\": \"\"\n"
                        "}")
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=messages,
            max_tokens=1000,  
            temperature=0.7
        )

        patient_case = json.loads(response.choices[0].message.content)

        return patient_case
    except Exception as e:
        return {"error": str(e)}

# SBAR report (Situation, Background, Assesment, Recommendation)
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

def chat_with_patient(user_input, patient_case):
    # Build the context from the patient case
    context = {
        "Situation": f"{patient_case['Symptoms']}.",
        "Background": f"{patient_case['Patient History']}.",
        "Assessment": f"{patient_case['Physical Examination Findings']}.",
    }
    
    # Prepare the messages for the OpenAI API
    messages = [
        {"role": "system", "content": "You are a patient speaking to a medical doctor about your medical problems."},
        {"role": "user", "content": json.dumps(context)},  # Ensure context is JSON serialized
        {"role": "user", "content": user_input}  # User input is kept as a string
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the desired model
            messages=messages,
            max_tokens=150,  # Adjust as necessary
            temperature=0.7
        )
        
        # Extract and return the response content
        patient_response = response.choices[0].message.content.strip()
        return {"response": patient_response}  # Return as a dictionary
    except Exception as e:
        return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    # Generate a patient case first (from the previous code)
    json_file_path = '../../media/icd10_diagnoses.json'  # Adjust the path as necessary
    diagnoses = load_diagnoses(json_file_path)
    
    case = generate_patient_case(diagnoses)
    # print("Generated Patient Case:\n", case)

    sbar = generate_sbar_report(case)
    # print("Generated Patient SBAR:\n", sbar)

    # Chat with the patient
    user_query = "What is your pain level on a scale of 1 to 10?"
    response = chat_with_patient(user_query, case)
    print("\nChatbot Response:\n", response)

