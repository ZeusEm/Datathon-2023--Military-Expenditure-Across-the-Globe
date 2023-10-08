# -*- coding: utf-8 -*-
"""
College of Defence Management - Datathon-2023
Theme: Military Expenditure across the Globe
"""
import pandas as pd

# Define the file path to the Excel file
file_path = r'D:\Projects\datathon23\datasets\Financial_Value-Arms_Exports.xlsx'

# Load the Excel file and get the list of worksheet names
xls = pd.ExcelFile(file_path)
worksheet_names = xls.sheet_names

# Print the list of worksheet names to verify
print("Worksheet Names:", worksheet_names)

# Define the desired worksheets
desired_worksheets = ['Local Currency', 'Current USD', 'Constant USD']

# Initialize dictionaries to store DataFrames
local_currency_df = {}
current_usd_df = {}
constant_usd_df = {}

dataframes = {}

# Load the desired worksheets and store them in DataFrames
for worksheet in desired_worksheets:
    if worksheet in worksheet_names:
        df = pd.read_excel(file_path, sheet_name=worksheet)
        if worksheet == 'Local Currency':
            local_currency_df = df
        elif worksheet == 'Current USD':
            current_usd_df = df
        elif worksheet == 'Constant USD':
            constant_usd_df = df
    else:
        print(f"Worksheet '{worksheet}' not found in the Excel file.")

# Check the structure of the DataFrames
print("Local Currency DataFrame:")
print(local_currency_df.head())

print("\nCurrent USD DataFrame:")
print(current_usd_df.head())

print("\nConstant USD DataFrame:")
print(constant_usd_df.head())

# Check for missing values in each DataFrame
print("Missing Values in Local Currency DataFrame:")
print(local_currency_df.isnull().sum())

print("\nMissing Values in Current USD DataFrame:")
print(current_usd_df.isnull().sum())

print("\nMissing Values in Constant USD DataFrame:")
print(constant_usd_df.isnull().sum())

# Check for data types and general information about each DataFrame
print("\nData Types and Info for Local Currency DataFrame:")
print(local_currency_df.info())

print("\nData Types and Info for Current USD DataFrame:")
print(current_usd_df.info())

print("\nData Types and Info for Constant USD DataFrame:")
print(constant_usd_df.info())

# Check basic statistics for each DataFrame
print("\nBasic Statistics for Local Currency DataFrame:")
print(local_currency_df.describe())

print("\nBasic Statistics for Current USD DataFrame:")
print(current_usd_df.describe())

print("\nBasic Statistics for Constant USD DataFrame:")
print(constant_usd_df.describe())

"""
Based on the output, it appears that there are multiple issues with the data in the 'Local Currency' worksheet:

    1. The first few rows contain metadata and header information. We should skip these rows when loading the data.
    2. There are many missing values represented as 'NaN' or '. .' in the dataset.
    3. The data types for most columns are 'object,' which may not be appropriate for numerical analysis.

The code below addresses these issues by skipping rows, handling missing values, and ensuring proper data types
"""

# Load the 'Local Currency' worksheet and skip the first few rows (skiprows)
local_currency_df = pd.read_excel(file_path, sheet_name='Local Currency', skiprows=4)

# Replace '. .' and other placeholders for missing values with NaN
local_currency_df = local_currency_df.replace('. .', pd.NA)

# Handle missing values based on your analysis needs (e.g., imputation or removal)
# Consider why data is missing. If it's missing completely at random (MCAR), meaning the probability of data being missing is unrelated to the values themselves, dropping rows may be a reasonable option. However, if the missing data is not MCAR (e.g., missing systematically or based on certain conditions), dropping rows might lead to biased results.
# For example, you can drop rows with missing values:
# local_currency_df = local_currency_df.dropna()

# Convert columns to appropriate data types as needed
# For example, if you have numerical columns, you can convert them to float or int:
# local_currency_df['Column_Name'] = local_currency_df['Column_Name'].astype(float)

# Check the structure of the cleaned DataFrame
print("Cleaned Local Currency DataFrame:")
print(local_currency_df.head())

# Check for missing values and data types in the cleaned DataFrame
print("\nMissing Values in Cleaned Local Currency DataFrame:")
print(local_currency_df.isnull().sum())

print("\nData Types and Info for Cleaned Local Currency DataFrame:")
print(local_currency_df.info())

# Check basic statistics for the cleaned DataFrame
print("\nBasic Statistics for Cleaned Local Currency DataFrame:")
print(local_currency_df.describe())

# Rename columns
new_column_names = ['Country', 'Currency'] + [f'Year_{year}' for year in range(1994, 2020)] + ['Explanation of data', 'Comments', 'Sources of data']
local_currency_df.columns = new_column_names

# Convert numeric columns to appropriate data types
numeric_columns = new_column_names[2:-3]  # Columns from Year_1994 to Year_2019
local_currency_df[numeric_columns] = local_currency_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Check the structure and data types after cleaning
print("Cleaned and Renamed Local Currency DataFrame:")
print(local_currency_df.head())
print("\nData Types and Info for Cleaned Local Currency DataFrame:")
print(local_currency_df.info())
