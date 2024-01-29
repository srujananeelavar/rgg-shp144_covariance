import pandas as pd

# Get input Excel file path from the user
input_path = input("Enter the path to the input Excel file: ")

# Read the Excel file
df = pd.read_excel(input_path)

# Filter rows with conservation score >= 0.90
high_score_df = df[df['Conservation Score'] >= 0.90]

# Filter rows with conservation score < 0.90
low_score_df = df[df['Conservation Score'] < 0.90]

# Get output paths from the user
high_score_output_path = input("Enter the path to save the high conservation score data: ")
low_score_output_path = input("Enter the path to save the low conservation score data: ")

# Write filtered data to separate Excel files
high_score_df.to_excel(high_score_output_path, index=False)
low_score_df.to_excel(low_score_output_path, index=False)

print("Data has been filtered and saved successfully!")
