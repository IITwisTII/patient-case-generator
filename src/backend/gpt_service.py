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

# Load the ICD-10 diagnoses from the JSON file
def load_diagnoses(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Function to generate a random patient case based on a random diagnosis
def generate_patient_case(diagnoses):

    # Pick a random diagnosis
    diagnosis = random.choice(diagnoses)

    # Create a prompt for the API
    messages = [
        {"role": "system", "content": "You are a medical expert helping to generate detailed medical cases."},
        {
            "role": "user",
            "content": f"Generate a detailed medical case for a patient diagnosed with \"{diagnosis}\". "
                       "Include the patient's history, symptoms, examination findings, test results, and treatment plan."
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or any other GPT model
            messages=messages,
            max_tokens=500,  # Adjust depending on the response size
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    # Path to your JSON file
    json_file_path = 'media/icd10_diagnoses.json'  # Adjust the path as necessary
    diagnoses = load_diagnoses(json_file_path)
    
    # Generate a patient case
    case = generate_patient_case(diagnoses)
    print("Generated Patient Case:\n", case)
