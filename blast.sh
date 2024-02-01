#!/bin/bash

# Ask user for the directory containing the .fasta files (database directory)
read -p "Enter the path to the directory containing the .fasta files (your database folder): " database_dir

# Check if the directory exists
if [ ! -d "$database_dir" ]; then
    echo "Error: Database directory not found."
    exit 1
fi

# User gives the path to search sequence file
read -p "Enter the path to search sequence .fasta file: " searchseq_file

# Check if search sequence .fasta file exists
if [ ! -f "$searchseq_file" ]; then
    echo "Error: Search sequence fasta file not found."
    exit 1
fi

# Ask user for the output directory
read -p "Enter the path to the directory where you want to store the blast output: " output_dir

# Create output directory if it doesn't exist
mkdir -p "$output_dir/blast_output"

# Execute blastn for each .fasta file in the database directory
for f in "$database_dir"/*.fa; do
    blastn -query "$searchseq_file" -subject "$f" -out "$output_dir/blast_output/$(basename "$f").out"
done

echo "Blastn execution completed."
