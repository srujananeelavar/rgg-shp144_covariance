from Bio import SeqIO
import pandas as pd

def fasta_to_excel(fasta_file, excel_file):
    # Parse the FASTA file and extract ID and sequence data
    records = SeqIO.parse(fasta_file, "fasta")
    data = {"ID": [], "Sequence": []}
    for record in records:
        data["ID"].append(record.id)
        data["Sequence"].append(str(record.seq))

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Write DataFrame to an Excel file
    df.to_excel(excel_file, index=False)

if __name__ == "__main__":
    # Get input and output file paths from the user
    input_fasta_file = input("Enter the input FASTA file path to be converted to excel: ")
    output_excel_file = input("Enter the output Excel file path with file name: ")

    # Convert the FASTA file to Excel
    fasta_to_excel(input_fasta_file, output_excel_file)
