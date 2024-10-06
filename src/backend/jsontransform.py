import json
import re

json_file_path =  "../../media/icd10_diagnoses.json"

with open(json_file_path, 'r') as file:
    data = json.load(file)

icd_10_code_pattern = re.compile("")
infectious_diseases = re.findall()

# Print the data
print(data[2])