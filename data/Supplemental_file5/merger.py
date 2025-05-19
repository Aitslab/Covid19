import json
import glob
import re
import os

# Adjust this path to your JSON files
folder_path = "DVVM/"
json_files = glob.glob(os.path.join(folder_path, "*.json"))

# Function to extract number from filename
def extract_number(filename):
    match = re.search(r'(\d+)', os.path.basename(filename))
    return int(match.group(1)) if match else float('inf')

# Sort files based on the extracted number
sorted_files = sorted(json_files, key=extract_number)

merged_data = []

# Read and append each JSON file
for file in sorted_files:
    with open(file, 'r', encoding='utf-8') as f:
        print(file)
        data = json.load(f)
        merged_data.append(data)

# Write the merged JSON to a new file
with open("DVVM_merged.json", 'w', encoding='utf-8') as out_file:
    json.dump(merged_data, out_file, indent=4, ensure_ascii=False)