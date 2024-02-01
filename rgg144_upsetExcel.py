import pandas as pd
import os

# Function to read contents of a FASTA file and return a dictionary
def read_fasta_to_dict(file_path):
    sequence_dict = {}
    with open(file_path, 'r') as file:
        header = ""
        sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if header and sequence:
                    sequence_dict[header] = sequence
                header = line[1:]
                sequence = ""
            else:
                sequence += line
        if header and sequence:
            sequence_dict[header] = sequence
    return sequence_dict

# Directory containing the FASTA files
directory = "/Users/srujananeelavar/Documents/Summer2023/Research/Rgg144RiosSHP/spn39DB_GoldenSet_7548Genomes_2023/"

# Get a list of all files in the directory
files = os.listdir(directory)

# Filter out only the files with the .fasta extension
fasta_files = [file for file in files if file.endswith(".fasta")]

# Extract file names without the .fasta extension
file_names = [file[:-6] for file in fasta_files]

# Create a DataFrame with the file names (without .fasta extension)
df = pd.DataFrame({"GoldenSet": file_names})

# Paths to Rgg FASTA files
rgg_fasta_path = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/alleles/D39_rgg144_alleles.fasta"

# Read contents of Rgg and Shp FASTA files into dictionaries
rgg_dict = read_fasta_to_dict(rgg_fasta_path)

# Add columns to df using rgg_dict values as column headers
for value in rgg_dict.values():
    df[value] = ''

# Export DataFrame to Excel
output_file_path = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/ExcelForUpset.xlsx"
df.to_excel(output_file_path, index=False)

print(f"DataFrame exported to {output_file_path}")


# Read the second Excel file
df2 = pd.read_excel("/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/blastParser_output/D39_rgg144_tophits_translated.xlsx")

# Iterate through each row in df
for index, row in df.iterrows():
    golden_set_value = row["GoldenSet"]
    
    # Check if the value exists in "ID" column of df2
    if golden_set_value in df2["ID"].values:
        # Get the corresponding row from df2
        matching_row = df2[df2["ID"] == golden_set_value].iloc[0]
        
        # Iterate through each column in df except "GoldenSet"
        for col in df.columns[1:]:
            # Get the value from "Sequence" column in df2
            sequence_value = matching_row["Sequence"]
            
            # Check if the column header matches the sequence_value
            if col == sequence_value:
                df.at[index, col] = 1
            else:
                df.at[index, col] = 0

# Save the modified DataFrame to the same Excel file
df.to_excel(output_file_path, index=False)

print("Excel file updated successfully!")

import pandas as pd

# Read the third Excel file
df3 = pd.read_excel("/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/alleles/rgg144_other_alleles_ID.xlsx")

# Read the existing Excel file
output_file_path = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/ExcelForUpset.xlsx"
df = pd.read_excel(output_file_path)

# Create a new column "R-Other" initialized with 0
df["R-Other"] = 0

# Iterate through each row in df
for index, row in df.iterrows():
    golden_set_value = row["GoldenSet"]
    
    # Check if the value exists in "ID" column of df3
    if golden_set_value in df3["ID"].values:
        df.at[index, "R-Other"] = 1

# Save the modified DataFrame to the same Excel file
df.to_excel(output_file_path, index=False)

import pandas as pd

# Read the existing Excel file
output_file_path = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/ExcelForUpset.xlsx"
df = pd.read_excel(output_file_path)

# Iterate through columns 2 to the second-to-last column
for col_index in range(1, len(df.columns) - 1):
    # Get the current column name
    current_col_name = df.columns[col_index]
    
    # Replace the column name with the corresponding key from rgg_dict
    df.rename(columns={current_col_name: list(rgg_dict.keys())[col_index - 1]}, inplace=True)

# Save the modified DataFrame to the same Excel file
df.to_excel(output_file_path, index=False)

print("Column headers updated successfully!")