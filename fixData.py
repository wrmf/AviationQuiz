import csv

# Function to replace the first character after a parenthesis
def replace_chars(text):
    if "AK" in text or "HI" in text:
        return text.replace('(', '(P', 1)
    else:
        return text.replace('(', '(K', 1)

# Input and output file names
input_file = 'airports.txt'  # Replace with the actual input file name
output_file = 'static/codes.csv'  # Replace with the desired output file name

# Open the input and output CSV files
with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Process each cell in the row and apply the replacement
        modified_row = [replace_chars(cell) for cell in row]
        writer.writerow(modified_row)

print(f'Results written to {output_file}')
