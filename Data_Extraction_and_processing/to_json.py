import re
import json

# Function to check if a line is a heading (all caps)
def is_heading(line):
    return line.isupper() and len(line.split()) <= 5  # Heading condition: all caps and typically short

# Function to read the file and format it into extracted portions
def extract_portions(file_path):
    extracted_portions = []
    
    # Open and read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    current_portion = ""
    list_pattern = re.compile(r'^[\d]+\..*|^[ivxlcdmIVXLCDM]+\..*|^[a-zA-Z]\..*|^[-*].*')  # Pattern to detect lists
    
    for i, line in enumerate(lines):
        # Strip leading and trailing whitespaces
        line = line.strip()
        
        # If the line is not empty
        if line:
            # Handle headings: Merge headings (all caps) with the next line
            if is_heading(line):
                current_portion += " " + line  # Append heading
                continue  # Skip adding the heading as a separate portion
            
            # If the line matches list patterns (numbered or bullet points), append to the current portion
            if list_pattern.match(line):
                current_portion += " " + line
            else:
                # Check for full stop and not splitting mid list or sections
                if current_portion and line.endswith('.'):
                    current_portion += " " + line
                    extracted_portions.append({"extracted_portion": current_portion.strip()})
                    current_portion = ""
                else:
                    # Otherwise, just keep adding the line to the current portion
                    current_portion += " " + line
    
    # Append the last portion if exists
    if current_portion:
        extracted_portions.append({"extracted_portion": current_portion.strip()})

    return extracted_portions

# Function to write the output to a JSON file
def write_to_json(output_path, extracted_portions):
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_portions, json_file, indent=4, ensure_ascii=False)

# Main function to execute the script
if __name__ == "__main__":
    input_file = "corrected_final.txt"  # Change this to your actual file path
    output_file = "output.json"

    extracted_data = extract_portions(input_file)
    write_to_json(output_file, extracted_data)

    print(f"Data has been extracted and written to {output_file}.")
