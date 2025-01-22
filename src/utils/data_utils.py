import json

def load_diagnoses(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        categorized_data = json.load(file)
    
    # Flatten the data into a list of dictionaries with 'category', 'code', and 'description'
    diagnoses = []
    for category, codes in categorized_data.items():
        for entry in codes:
            # Assuming each entry is a dictionary like {"code": "description"}
            for code, description in entry.items():
                diagnoses.append({
                    "category": category,
                    "code": code,
                    "description": description
                })
    return diagnoses