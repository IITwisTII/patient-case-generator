import json
from .response_generator import generate_openai_response

def perform_medical_test(client, user_input, patient_case, history):
    system_prompt = (
        "You are a medical expert performing medical tests on a patient. "
        f"This is what has been said so far: '{history}' "
        "The patient has a medical condition, but you are not to reveal the diagnosis. "
        "Instead, you will provide test results that are consistent with the patient's condition."
    )
    
    # Create context based on the patient's information (without revealing diagnosis)
    context = {
        "Symptoms": patient_case["Symptoms"],
        "Patient History": patient_case["Patient History"],
        "Physical Examination Findings": patient_case["Physical Examination Findings"]
    }
    context_json = json.dumps(context)

    # Generate the response based on the test input
    response = generate_openai_response(client, system_prompt, [context_json, user_input])
    
    print("Test Results:", response)
    return response
