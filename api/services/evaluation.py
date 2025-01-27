from .response_generator import generate_openai_response

def evaluate_diagnosis(client, patient_case, chat_history):

    filtered_chat_history = [entry for entry in chat_history if "User" in entry]

    system_prompt = (
        "You are a medical expert tasked with evaluating a doctor's diagnostic and decision-making process. "
        "Focus exclusively on the doctor's observations, diagnostic reasoning, tests ordered, and treatment plan. "
        "You must evaluate whether the doctor's final diagnosis is accurate based on the provided patient case. "
        "If the diagnosis is completely inappropriate for the patient's symptoms and condition, flag it as an error. "
        "Provide detailed feedback and assign a score out of 10 based on the accuracy and thoroughness of the doctor's approach."
        "Your job is to focus **only** on the doctor's reasoning as displayed through their statements and actions. "
        "Do not refer to the patient's background, physical exam, or tests unless the doctor specifically mentions them in their diagnostic reasoning. "
        "Evaluate how well the doctor came to their diagnosis based on their reasoning and actions. "
        "If no reasoning or appropriate actions (e.g., ordering tests, performing a physical exam) are given to support the diagnosis, note that in your evaluation."
    )
    
    feedback_prompt = (
        f"Patient Case (Background): {patient_case}\n"
        f"Doctor's Diagnosis and Decision-Making: {filtered_chat_history}\n"
        "Evaluate the doctor's diagnostic reasoning based on their decision-making in response to the patient's case. "
        "This includes their reasoning for ordering specific tests, their analysis of the symptoms, and their treatment plan. "
        "Check if the diagnosis is aligned with the patient's symptoms and condition. "
        "If the doctor made an incorrect diagnosis (e.g., feet for a head injury), provide feedback on why it was incorrect. "
        "Evaluate the overall accuracy of the diagnosis based on the doctor's reasoning and actions and rate their performance accordingly. "
        "Rate the doctor's overall performance from 0 to 10 based on the clinical decision-making and correctness of the diagnosis."
    )
    
    response = generate_openai_response(client, system_prompt, [feedback_prompt])
    
    print("API Response:", response)
    return response