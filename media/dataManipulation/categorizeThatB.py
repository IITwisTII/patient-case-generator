import json

# Function to categorize ICD codes by chapter
def categorize_by_chapter(icd_data):
    chapters = {
        "A": "Infectious and parasitic diseases",
        "B": "Infectious and parasitic diseases",
        "C": "Neoplasms",
        "D": "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism",
        "E": "Endocrine, nutritional and metabolic diseases",
        "F": "Mental, Behavioral and Neurodevelopmental disorders",
        "G": "Diseases of the nervous system",
        "H": "Diseases of the eye and adnexa",
        "I": "Diseases of the circulatory system",
        "J": "Diseases of the respiratory system",
        "K": "Diseases of the digestive system",
        "L": "Diseases of the skin and subcutaneous tissue",
        "M": "Diseases of the musculoskeletal system and connective tissue",
        "N": "Diseases of the genitourinary system",
        "O": "Pregnancy, childbirth and the puerperium",
        "P": "Certain conditions originating in the perinatal period",
        "Q": "Congenital malformations, deformations and chromosomal abnormalities",
        "R": "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified",
        "S": "Injury, poisoning and certain other consequences of external causes",
        "T": "Injury, poisoning and certain other consequences of external causes",
        "U": "Codes for special purposes",
        "V": "External causes of morbidity",
        "W": "External causes of morbidity",
        "X": "External causes of morbidity",
        "Y": "External causes of morbidity",
        "Z": "Factors influencing health status and contact with health services"
    }

    categorized_data = {chapter: [] for chapter in chapters.values()}  # Initialize empty lists for each chapter
    
    # Iterate through the ICD data and categorize based on the first letter of the code
    for code, description in icd_data.items():
        first_letter = code[0]  # Get the first letter of the code
        if first_letter in chapters:  # Check if the letter matches a chapter
            chapter_name = chapters[first_letter]
            categorized_data[chapter_name].append({code: description})

    return categorized_data

# Load the original ICD data from the JSON file
input_file_path = 'media/parsed_icd_data.json'  # Replace with the actual path to your parsed data
with open(input_file_path, 'r', encoding='utf-8') as file:
    icd_data = json.load(file)

# Categorize the data by chapter
categorized_icd_data = categorize_by_chapter(icd_data)

# Save the categorized data to a new JSON file
output_file_path = 'media/categorized_icd_data.json'  # Path for the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(categorized_icd_data, file, ensure_ascii=False, indent=2)

print(f"Categorized data has been saved to {output_file_path}")
