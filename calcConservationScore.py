from Bio import AlignIO
from collections import Counter
import pandas as pd

# Get input and output paths from the user
input_path = input("Enter the path to the input FASTA file: ")
output_path = input("Enter the path to save the output Excel file: ")

# Load the multiple sequence alignment from the input file
alignment = AlignIO.read(input_path, "fasta")

# Get the length of the alignment
alignment_length = alignment.get_alignment_length()

# Calculate the conservation scores and residue counts
output_data = []
all_residues = set()

for position in range(alignment_length):
    column = alignment[:, position]
    residue_counts = Counter(column)
    most_common_residue, most_common_count = residue_counts.most_common(1)[0]
    conservation_score = (most_common_count / len(column))
    residue_counts['Position'] = position + 1
    residue_counts['Conservation Score'] = conservation_score
    residue_counts['Most Common Residue'] = most_common_residue
    output_data.append(residue_counts)
    all_residues.update(residue_counts.keys())

# Fill missing residues with 0
for data in output_data:
    for residue in all_residues:
        if residue not in data:
            data[residue] = 0

# Create a DataFrame with residue counts, conservation scores, and most common residue
df = pd.DataFrame(output_data)

# Rearrange columns to have "Position" as the first column
columns = ['Position', 'Most Common Residue'] + [col for col in df.columns if col != 'Position' and col != 'Conservation Score' and col != 'Most Common Residue'] + ['Conservation Score']
df = df[columns]

# Write the DataFrame to the output Excel file
df.to_excel(output_path, index=False)

print("Conservation analysis completed and saved to:", output_path)