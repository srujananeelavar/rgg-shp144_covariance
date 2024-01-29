def read_fasta(file_path):
    sequences = {}
    with open(file_path, 'r') as fasta_file:
        header = ''
        sequence = ''
        for line in fasta_file:
            if line.startswith('>'):
                header = line.strip()  # Store the entire header line
                sequence = ''  # Reset sequence for the new header
            else:
                sequence += line.strip()
                sequences[header] = sequence  # Store sequence under the complete header
    return sequences

def write_fasta(sequences, order, output_file):
    with open(output_file, 'w') as fasta_output:
        for index in order:
            header_to_find = f">{index} "  # Note the space after index
            found = False
            for header, sequence in sequences.items():
                if header.startswith(header_to_find):
                    fasta_output.write(f"{header}\n{sequence}\n")
                    found = True
                    break
            if not found:
                print(f"Warning: Sequence with header {header_to_find.strip()} not found in input file.")

def main():
    input_file = input("Enter the path to the input FASTA file: ")
    output_file = input("Enter the path to the output FASTA file: ")
    order_str = input("Enter the desired order of sequences separated by commas: ")
    order = [int(index) for index in order_str.split(',')]

    sequences = read_fasta(input_file)
    if not sequences:
        print("Error: Input FASTA file is empty or could not be read.")
        return

    write_fasta(sequences, order, output_file)
    print("Sequences reordered and written to output file successfully!")

if __name__ == "__main__":
    main()
