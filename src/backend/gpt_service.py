from openai import OpenAI
import os
import json
import random
from dotenv import load_dotenv

# Set your OpenAI API key
openai.api_key = os.getenv("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")

client = OpenAI()

# Load the ICD-10 diagnoses from the JSON file
def load_diagnoses(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Function to generate a random patient case based on a random diagnosis
def generate_patient_case(diagnoses):
    # Pick a random diagnosis

    diagnosis = random.choice(diagnoses)

    # Create a prompt for the API
    prompt = (f"Generate a detailed medical case for a patient diagnosed with \"{diagnosis}\". "
              "Include the patient's history, symptoms, examination findings, test results, and treatment plan.")

    try:
        response = client.chat.Completion.create(
            model="gpt-4",  # or any other GPT model
            prompt=prompt,
            max_tokens=500,  # Adjust depending on the response size
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

# Example usage
if __name__ == "__main__":
    # Path to your JSON file
    json_file_path = '../../media/icd10_diagnoses.json'  # Adjust the path as necessary
    diagnoses = load_diagnoses(json_file_path)
    
    # Generate a patient case
    case = generate_patient_case(diagnoses)
    print("Generated Patient Case:\n", case)
