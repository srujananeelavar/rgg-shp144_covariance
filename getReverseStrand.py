import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq

# Prompt user for input and output file paths
excel_file_path = input("Enter the path to the Excel file: ")
fasta_file_path = input("Enter the path to the multi-sequence fasta file: ")
output_sequences_path = input("Enter the path for the output sequences fasta file: ")
output_reverse_complement_path = input("Enter the path for the output reverse complement sequences fasta file: ")
user_sequence = input("Enter the sequence to search for: ")

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file_path)

# Filter DataFrame to get corresponding IDs
filtered_df = df[df['Sequence'] == user_sequence]

# Remove '_1' from the end of IDs
filtered_df.loc[:, 'ID'] = filtered_df['ID'].apply(lambda x: x[:-2])

# Get unique IDs
ids = filtered_df['ID'].unique()

# Read the multi-sequence fasta file
fasta_sequences = SeqIO.parse(open(fasta_file_path), 'fasta')

# Initialize lists to store sequences and reverse complement sequences
sequences = []
reverse_complement_sequences = []

# Iterate over fasta sequences
for fasta in fasta_sequences:
    header = fasta.id
    sequence = str(fasta.seq)
    # Check if header contains any of the IDs
    for id in ids:
        if id in header:
            sequences.append((header, sequence))
            reverse_complement_sequences.append((header, str(Seq(sequence).reverse_complement())))

# Write sequences to fasta file
with open(output_sequences_path, 'w') as f:
    for header, sequence in sequences:
        f.write(f'>{header}\n{sequence}\n')

# Write reverse complement sequences to fasta file
with open(output_reverse_complement_path, 'w') as f:
    for header, sequence in reverse_complement_sequences:
        f.write(f'>{header}\n{sequence}\n')

print("Sequences extracted and written to files successfully.")
