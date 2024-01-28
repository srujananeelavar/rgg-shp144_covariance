import pandas as pd

# Read the Excel file into a pandas DataFrame
df = pd.read_excel("/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/alleles/D39rgg144_sigalleles_count_filtered.xlsx")

fasta_content = ""
for i, (allele, frequency) in enumerate(zip(df['Alleles'], df['Frequency']), start=1):
    fasta_content += f">{i} ({frequency})\n{allele}\n"

# Write content to a FASTA file
with open("/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/alleles/D39_rgg144_alleles.fasta", "w") as fasta_file:
    fasta_file.write(fasta_content)

print("FASTA file generated successfully!")