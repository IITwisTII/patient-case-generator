import json

# Function to parse the ICD data
def parse_icd_data(data):
    icd_dict = {}
    current_code = ""
    current_description = []
    
    for line in data:
        if line.strip() == "":
            continue
        
        # If a line contains a code, process the previous entry (if any) and reset
        if line[:5].isalnum():
            if current_code:
                icd_dict[current_code] = " ".join(current_description)
            
            # Start a new code and description
            current_code, description = line[:5].strip(), line[5:].strip()
            current_description = [description]
        else:
            # This line is part of the description, add it to the current description
            current_description.append(line.strip())
    
    # Add the last code-description pair
    if current_code:
        icd_dict[current_code] = " ".join(current_description)
    
    return icd_dict

# Load the JSON data from the input file
input_file_path = 'media/icd10_diagnoses.json'  # Replace with the actual path to your JSON file
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Parse the data
icd_data = parse_icd_data(data)

# Output the parsed dictionary
output_file_path = 'media/parsed_icd_data.json'  # Path for the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(icd_data, file, ensure_ascii=False, indent=2)

print(f"Parsed data has been saved to {output_file_path}")
