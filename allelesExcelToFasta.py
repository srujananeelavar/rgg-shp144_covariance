import pandas as pd

# Get input file path from the user
input_file_path = input("Enter the path of the input Excel file: ")

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(input_file_path)

# Get output file path from the user
output_file_path = input("Enter the path of the output FASTA file: ")

fasta_content = ""
for i, (allele, frequency) in enumerate(zip(df['Alleles'], df['Frequency']), start=1):
    fasta_content += f">{i} ({frequency})\n{allele}\n"

# Write content to the FASTA file
with open(output_file_path, "w") as fasta_file:
    fasta_file.write(fasta_content)

print("FASTA file generated successfully at:", output_file_path)
