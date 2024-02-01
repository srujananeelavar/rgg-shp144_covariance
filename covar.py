def parse_fasta(filename):
    sequences = {}
    with open(filename, 'r') as file:
        sequence = ''
        header = None
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if header:
                    seq_num = int(header.split()[0])  # Extract sequence number
                    sequences[seq_num] = sequence
                header = line[1:]
                sequence = ''
            else:
                sequence += line
        if header:  # Process last sequence
            seq_num = int(header.split()[0])
            sequences[seq_num] = sequence
    return sequences

def analyze_groups(sequences, groups, output_file):
    with open(output_file, 'w') as f:
        # Write groups as tab-separated values in the first line
        f.write("\t".join(["Group " + str(i) for i in range(1, len(groups) + 1)]) + "\n")

        max_length = len(list(sequences.values())[0])
        for position in range(max_length):
            f.write("Position " + str(position + 1) + ": ")
            f.write("\t")
            for group in groups:
                for seq_num in group:
                    f.write(sequences.get(seq_num, '-')[position] + " ")  # Use .get() to handle missing sequences
                f.write("\t")
            f.write("\n")

fasta_file = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/rgg144VarPos/Rgg144VarPosAlleles.fasta"  # Update with your file name
groups = [[3,1,8,9,20], [5,6], [2, 7, 13, 16, 10], [4,15], [1], [14], [11, 18], [19],[12]]  
output_file = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/rgg144VarPos/covar_rgg_shp.tsv"  # Update with your desired output file name

sequences = parse_fasta(fasta_file)
analyze_groups(sequences, groups, output_file)
