import json
from collections import defaultdict

# Function to merge categories with the same name
def merge_categories(categorized_data):
    merged_data = defaultdict(list)

    for category, codes in categorized_data.items():
        # Add all codes from the category into the corresponding category in merged_data
        merged_data[category].extend(codes)
    
    return dict(merged_data)  # Convert defaultdict back to a regular dict for output

# Load the categorized ICD data from the JSON file
input_file_path = 'media/categorized_icd_data.json'  # Replace with the actual path to your categorized data
with open(input_file_path, 'r', encoding='utf-8') as file:
    categorized_icd_data = json.load(file)

# Merge the categories with the same name
merged_icd_data = merge_categories(categorized_icd_data)

# Save the merged data to a new JSON file
output_file_path = 'media/final_icd_data.json'  # Path for the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(merged_icd_data, file, ensure_ascii=False, indent=2)

print(f"Merged data has been saved to {output_file_path}")
