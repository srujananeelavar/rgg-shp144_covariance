import pandas as pd
from Bio import SeqIO

# Get input paths from user
positions_file = input("Enter the path to the Excel file containing positions: ")
aligned_fasta_file = input("Enter the path to the multi-sequence FASTA file: ")

# Read the positions from the Excel file
positions_df = pd.read_excel(positions_file)
positions_list = positions_df['Position'].tolist()
print(positions_list)

# Read the multi-sequence FASTA file
sequences = SeqIO.parse(aligned_fasta_file, 'fasta')

# Process each sequence and create modified sequences
modified_sequences = []
for sequence in sequences:
    seq_id = sequence.id.split()[0]
    description = sequence.description.split()[1:]
    modified_seq = ''.join([sequence.seq[pos-1] for pos in positions_list if 1 <= pos <= len(sequence.seq)])
    modified_header = f'>{seq_id} {" ".join(description)}'
    modified_sequence = f'{modified_header}\n{modified_seq}\n'
    modified_sequences.append(modified_sequence)

# Get output path from user
output_fasta = input("Enter the path to save the modified FASTA file: ")

# Write modified sequences to a new FASTA file
with open(output_fasta, 'w') as output_file:
    output_file.writelines(modified_sequences)
