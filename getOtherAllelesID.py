import pandas as pd

# Path to the first Excel file
excel1_path = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/alleles/rgg144_other_alleles.xlsx"

# Path to the second Excel file
excel2_path = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/blastParser_output/D39_rgg144_tophits_translated_altered.xlsx"

# Read both Excel files
df1 = pd.read_excel(excel1_path)
df2 = pd.read_excel(excel2_path)

# Retain rows in df2 where Allele entry equals Sequence entry
filtered_df2 = df2[df2['Sequence'].isin(df1['Alleles'])]

# Path to the output Excel file
output_excel_path = "/Users/srujananeelavar/Documents/Thesis/Rgg-SHP/rgg144/D39/alleles/rgg144_other_alleles_ID.xlsx"

# Write the filtered data to a new Excel file
filtered_df2.to_excel(output_excel_path, index=False)

print(filtered_df2)

print("Filtered data has been written to:", output_excel_path)

import pandas as pd

# Read both Excel files
df1 = pd.read_excel(excel1_path)
df2 = pd.read_excel(excel2_path)

# Merge df1 and df2 on 'Sequence' and 'Alleles' columns
joint_df = pd.merge(df1, df2, how='inner', left_on='Alleles', right_on='Sequence')

# Display or further process the joint DataFrame
print(joint_df)

