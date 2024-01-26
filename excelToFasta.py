import pandas as pd

# Get input file path from the user
excel_path = input("Enter the path to the Excel file: ")

# Get output file path from the user
fasta_path = input("Enter the path to the output FASTA file including file name: ")

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_path)

# Open the output fasta file for writing
with open(fasta_path, 'w') as f:
    # Loop through each row of the DataFrame
    for i, row in df.iterrows():
        # Write the fasta header line
        f.write('>' + str(row['Contig']) + '\n')
        # Write the sequence line(s)
        sequence = str(row['Sequence'])
        # Split the sequence into lines of 60 characters each
        sequence_lines = [sequence[j:j+60] for j in range(0, len(sequence), 60)]
        for line in sequence_lines:
            f.write(line + '\n')

print("Excel converted to FASTA!")