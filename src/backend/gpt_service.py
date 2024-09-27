import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_patient_case(prompt):
    try:
        response = openai.Completion.create(
            model="gpt-4",  # or any other GPT model
            prompt=prompt,
            max_tokens=500,  # Adjust depending on the response size
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)
