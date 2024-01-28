from Bio import SeqIO
import pandas as pd

def find_subsequence(seq, subseq):
    """
    Find occurrences of a subsequence within a sequence.
    Returns a list of tuples containing start position and the subsequence + 2 characters.
    """
    occurrences = []
    sub_len = len(subseq)
    for i in range(len(seq) - sub_len + 1):
        if seq[i:i+sub_len] == subseq:
            end = min(i + sub_len + 2, len(seq))
            occurrences.append((i, seq[i:end]))
    return occurrences

def main(fasta_file, subsequence, output_excel):
    # Read FASTA file
    records = list(SeqIO.parse(fasta_file, "fasta"))

    # Initialize DataFrame to store results
    df = pd.DataFrame(columns=['Header', 'Occurrence'])

    # Search for subsequence in each sequence
    for record in records:
        occurrences = find_subsequence(str(record.seq), subsequence)
        for i, (start, occurrence) in enumerate(occurrences, start=1):
            header = f"{record.id}_{i}"
            df = pd.concat([df, pd.DataFrame({'Header': [header], 'Occurrence': [occurrence]})], ignore_index=True)

    # Write results to Excel
    df.to_excel(output_excel, index=False)
    print("Results saved to Excel file:", output_excel)

if __name__ == "__main__":
    # Get user input for file paths
    fasta_file = input("Enter the path to the input FASTA file with file name and extension: ")
    subsequence = input("Enter the subsequence to search for: ")
    output_excel = input("Enter the path for the output Excel file with file name and extension: ")

    main(fasta_file, subsequence, output_excel)
