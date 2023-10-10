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

"""
Based on the output, it appears that there are multiple issues with the data in the 'Local Currency' worksheet:

    1. The first few rows contain metadata and header information. We should skip these rows when loading the data.
    2. There are many missing values represented as 'NaN' or '. .' in the dataset.
    3. The data types for most columns are 'object,' which may not be appropriate for numerical analysis.

The code below addresses these issues by skipping rows, handling missing values, and ensuring proper data types
"""

# Load the worksheets and skip the first few rows (skiprows)
local_currency_df = pd.read_excel(file_path, sheet_name='Local Currency', skiprows=8)
current_usd_df = pd.read_excel(file_path, sheet_name='Current USD', skiprows=8)
constant_usd_df = pd.read_excel(file_path, sheet_name='Constant USD', skiprows=8)

# Replace '. .' and other placeholders for missing values with NaN
local_currency_df = local_currency_df.replace('. .', pd.NA)
current_usd_df = current_usd_df.replace('. .', pd.NA)
constant_usd_df = constant_usd_df.replace('. .', pd.NA)

def split_and_clean(df):
    # Initialize empty DataFrames for exports and licences
    df_exports = pd.DataFrame(columns=df.columns)
    df_licences = pd.DataFrame(columns=df.columns)

    # Initialize variables to store country name for licences
    current_country = None
    licences_to_append = []

    for index, row in df.iterrows():
        explanation = row['Explanation of data']

        # Check if explanation is not NaN
        if not pd.isna(explanation) and 'arms exports' in explanation.lower():
            # This row belongs to exports
            df_exports = pd.concat([df_exports, pd.DataFrame(row).transpose()], ignore_index=True)
            
            # Update current country for licences
            current_country = row['Country']
        elif not pd.isna(explanation) and 'arms export licences' in explanation.lower():
            # This row belongs to licences
            if current_country:
                # Add country name to the licences row
                row['Country'] = current_country
                df_licences = pd.concat([df_licences, pd.DataFrame(row).transpose()], ignore_index=True)
            else:
                # No corresponding country found for licences
                licences_to_append.append(row)

    # Append any remaining licence rows
    df_licences = pd.concat([df_licences, pd.DataFrame(licences_to_append)], ignore_index=True)

    return df_exports, df_licences

# Split and clean the Local Currency DataFrame
local_currency_exports_df, local_currency_licences_df = split_and_clean(local_currency_df)

# Split and clean the Current USD DataFrame
current_usd_exports_df, current_usd_licences_df = split_and_clean(current_usd_df)

# Split and clean the Constant USD DataFrame
constant_usd_exports_df, constant_usd_licences_df = split_and_clean(constant_usd_df)

# List of all dataframes
all_dataframes = [
    local_currency_exports_df, local_currency_licences_df,
    current_usd_exports_df, current_usd_licences_df,
    constant_usd_exports_df, constant_usd_licences_df
]

# Remove rows with "Country" as "nan" from all dataframes
for df in all_dataframes:
    df.dropna(subset=['Country'], inplace=True)
    df.reset_index(drop=True, inplace=True)

# Handle missing values based on your analysis needs (e.g., imputation or removal)
# Consider why data is missing. If it's missing completely at random (MCAR), meaning the probability of data being missing is unrelated to the values themselves, dropping rows may be a reasonable option. However, if the missing data is not MCAR (e.g., missing systematically or based on certain conditions), dropping rows might lead to biased results.
# For example, you can drop rows with missing values:
# local_currency_df = local_currency_df.dropna()

# Convert columns to appropriate data types as needed
# For example, if you have numerical columns, you can convert them to float or int:
# local_currency_df['Column_Name'] = local_currency_df['Column_Name'].astype(float)

# List of names for the corresponding dataframes
all_dataframe_names = [
    "Local Currency Exports", "Local Currency Licences",
    "Current USD Exports", "Current USD Licences",
    "Constant USD Exports", "Constant USD Licences"
]

# Define exchange rates for Dutch Guilders to Euros for each year
exchange_rates = {
    1994: 0.45378,
    1995: 0.45378,
    1996: 0.45378,
    1997: 0.45378,
    1998: 0.45378,
    1999: 0.45378,
    2000: 0.45378,
    2001: 0.45378,
    2002: 0.45378,
    2003: 0.45378,
    2004: 0.45378,
    2005: 0.45378,
    2006: 0.45378,
    2007: 0.45378,
    2008: 0.45378,
    2009: 0.45378,
    2010: 0.45378,
    2011: 0.45378,
    2012: 0.45378,
    2013: 0.45378,
    2014: 0.45378,
    2015: 0.45378,
    2016: 0.45378,
    2017: 0.45378,
    2018: 0.45378,
    2019: 0.45378,
}

# Iterate through the dataframe and convert Dutch Guilders to Euros
for year in range(1994, 2020):
    # Check if the year exists in the exchange_rates dictionary
    if year in exchange_rates:
        # Convert the values in Dutch Guilders to Euros
        local_currency_licences_df[year] = local_currency_licences_df.apply(
            lambda row: row[year] * exchange_rates[year] if row['Currency'] == 'D. Guilders (m.)' else row[year],
            axis=1
        )

# Remove rows with 'D. Guilders (m.)' in the 'Currency' column
local_currency_licences_df = local_currency_licences_df[local_currency_licences_df['Currency'] != 'D. Guilders (m.)']

# Iterate through dataframes and print summary information for each
for dataframe, name in zip(all_dataframes, all_dataframe_names):
    print(f"Summary for {name}:\n")

    # Print dataframe description
    print("Dataframe Description:")
    print(dataframe.describe())
    print("\n")
    
# Assuming your DataFrame is named 'local_currency_licences_df'
duplicate_rows = local_currency_licences_df[local_currency_licences_df.duplicated()]
print("Duplicate Rows:")
print(duplicate_rows)

local_currency_licences_df = local_currency_licences_df.drop_duplicates()
    
# Separate loop to print first few rows for each dataframe
for dataframe, name in zip(all_dataframes, all_dataframe_names):
    print(f"First Few Rows for {name}:\n")
    print(dataframe.head())
    print("\n")

# Separate loop to check for missing values and data types for each dataframe
for dataframe, name in zip(all_dataframes, all_dataframe_names):
    print(f"Missing Values for {name}:\n")
    print(dataframe.isnull().sum())
    print("\n")

    print(f"Dataframe Info for {name}:\n")
    print(dataframe.info())
    print("\n")

# Rename columns
new_column_names = ['Country', 'Currency'] + [f'Year_{year}' for year in range(1994, 2020)] + ['Explanation of data', 'Comments', 'Sources of data']
local_currency_df.columns = new_column_names

# Convert numeric columns to appropriate data types
numeric_columns = new_column_names[2:-3]  # Columns from Year_1994 to Year_2019
local_currency_df[numeric_columns] = local_currency_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Rename columns
new_column_names = ['Country'] + [f'Year_{year}' for year in range(2001, 2020)] + ['Explanation of data', 'Comments', 'Sources of data']
current_usd_df.columns = new_column_names

# Convert numeric columns to appropriate data types
numeric_columns = new_column_names[1:-3]  # Columns from Year_2001 to Year_2019
current_usd_df[numeric_columns] = current_usd_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Rename columns
new_column_names = ['Country'] + [f'Year_{year}' for year in range(2001, 2020)] + ['Explanation of data', 'Comments', 'Sources of data']
constant_usd_df.columns = new_column_names

# Convert numeric columns to appropriate data types
numeric_columns = new_column_names[1:-3]  # Columns from Year_2001 to Year_2019
constant_usd_df[numeric_columns] = constant_usd_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Check the structure and data types after cleaning
print("Cleaned and Renamed Local Currency DataFrame:")
print(local_currency_df.head())
print("\nData Types and Info for Cleaned Local Currency DataFrame:")
print(local_currency_df.info())

# Check the structure and data types after cleaning
print("Cleaned and Renamed Current USD DataFrame:")
print(current_usd_df.head())
print("\nData Types and Info for Cleaned Current USD DataFrame:")
print(current_usd_df.info())

# Check the structure and data types after cleaning
print("Cleaned and Renamed Constant USD DataFrame:")
print(current_usd_df.head())
print("\nData Types and Info for Cleaned Constant USD DataFrame:")
print(current_usd_df.info())

# Exploratory Data Analysis (EDA) commences

import matplotlib.pyplot as plt
import numpy as np

# Choose a country for analysis (e.g., Albania)
country = 'India'

# Filter the data for the selected country
country_data_local = local_currency_df[local_currency_df['Country'] == country]
country_data_current_usd = local_currency_df[local_currency_df['Country'] == country]
country_data_constant_usd = local_currency_df[local_currency_df['Country'] == country]

# Extract years and military expenditure values for the selected country
years = range(1994, 2020)
military_expenditure_local = np.nan_to_num(country_data_local.iloc[:, 2:29].values.flatten(), nan=0)
military_expenditure_current_usd = np.nan_to_num(country_data_current_usd.values.flatten()[1:], nan=0)
military_expenditure_constant_usd = np.nan_to_num(country_data_constant_usd.values.flatten()[1:], nan=0)

# Create a time series plot for military expenditure
plt.figure(figsize=(12, 6))
plt.plot(years, military_expenditure_local, label='Local Currency', marker='o')
plt.plot(years, military_expenditure_current_usd, label='Current USD', marker='o')
plt.plot(years, military_expenditure_constant_usd, label='Constant USD', marker='o')
plt.title(f'Military Expenditure Over Time for {country}')
plt.xlabel('Year')
plt.ylabel('Military Expenditure (Million USD)')
plt.xticks(years, rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
