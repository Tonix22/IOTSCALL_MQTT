import os

def clean_log_file(input_path, output_path):
    """
    Removes lines containing ' - ---- MQTT process started -------' from the input log file 
    and writes the cleaned log to the output file.
    """
    search_string = " - ---- MQTT process started -------"
    
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # Check if the line contains the search string
            if search_string not in line:
                outfile.write(line)

# Example usage:
if __name__ == "__main__":
    input_log_path = "report copy.log"
    output_log_path = "cleaned_output.log"
    
    clean_log_file(input_log_path, output_log_path)
    print(f"Cleaned log has been saved to: {output_log_path}")
