#!/bin/bash

# Check if EMBOSS transeq is installed
command -v transeq >/dev/null 2>&1 || {
    echo >&2 "EMBOSS transeq is not installed. Please install EMBOSS first. Aborting."
    exit 1
}

# Input FASTA file name
read -p "Enter the path to the input FASTA file that needs to be translated: " input_fasta

# Output file name for translated protein sequences
read -p "Enter the path to the output protein sequence file including the name of the file: " output_protein

echo "Translating $input_fasta to $output_protein..."

# Run transeq to translate the FASTA file
transeq -sequence "$input_fasta" -outseq "$output_protein"

echo "Translation completed. Protein sequences are stored in $output_protein."
