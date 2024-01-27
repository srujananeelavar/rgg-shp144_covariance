import pandas as pd
from openpyxl import Workbook

# Get the input Excel file path from the user
input_excel_file = input("Enter the path to your input Excel file: ")

# Load the Excel file
xls = pd.ExcelFile(input_excel_file)

# Create a new workbook to save all sheets into a single Excel file
workbook = Workbook()

# Loop through all sheets in the Excel file
for sheet_name in xls.sheet_names:
    # Load the sheet into a pandas DataFrame
    df = xls.parse(sheet_name)

    # Get the counts of each sequence in the 'Sequence' column
    counts = df['Sequence'].value_counts().reset_index()

    # Rename the columns to 'Alleles' and 'Counts'
    counts = counts.rename(columns={'index': 'Alleles', 'Sequence': 'Counts'})

    # Create a new sheet with the same data
    sheet = workbook.create_sheet(title=sheet_name)

    # Insert column headers as the first row
    headers = ["Alleles", "Counts"]
    sheet.append(headers)
    
    # Convert the pandas DataFrame to a list of lists for openpyxl
    data = counts.values.tolist()

    # Write the data to the new sheet
    for row in data:
        sheet.append(row)

# Remove the default sheet created and save the Excel file
workbook.remove(workbook.active)

# Get the output Excel file path from the user
output_excel_file = input("Enter the path to save the output Excel file with excel file name: ")

workbook.save(output_excel_file)

print("Allele frequency counted - Done!")
