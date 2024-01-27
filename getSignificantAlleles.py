# import pandas as pd

# # Read the input Excel sheet
# df = pd.read_excel('/Users/srujananeelavar/Documents/Summer2023/Research/Rgg144RiosSHP/SHP144/SHP144NT/SHP144AlleleCounts.xlsx')

# # Calculate the total count of Sequence
# total_count = df['Counts'].sum()

# # Filter out rows with counts less than 5% of the total
# df = df[df['Counts'] >= 0.01 * total_count]

# # Rename the columns to Alleles and Frequency
# df = df.rename(columns={'Alleles': 'Alleles', 'Counts': 'Counts'})

# # Write the filtered results to a new Excel sheet
# df.to_excel('/Users/srujananeelavar/Documents/Summer2023/Research/Rgg144RiosSHP/SHP144/SHP144NT/SHP144Sig1PercentAlleleCounts.xlsx', index=False)
import pandas as pd

# Prompt the user to input the file path for the input Excel sheet
input_file_path = input("Enter the file path for the input Excel sheet: ")

# Read the input Excel sheet
df = pd.read_excel(input_file_path)

# Calculate the total count of Sequence
total_count = df['Counts'].sum()

# Filter out rows with counts less than 5% of the total
df = df[df['Counts'] >= 0.01 * total_count]

# Prompt the user to input the file path for the output Excel sheet
output_file_path = input("Enter the file path for the output Excel sheet: ")

# Rename the columns to Alleles and Frequency (assuming these are the desired column names)
df = df.rename(columns={'Alleles': 'Alleles', 'Counts': 'Frequency'})

# Write the filtered results to a new Excel sheet
df.to_excel(output_file_path, index=False)

print("Filtered data has been written to the specified output Excel sheet.")
