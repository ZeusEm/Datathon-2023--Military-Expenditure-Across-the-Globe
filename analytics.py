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

# List of dataframes and their corresponding names
dataframes = [local_currency_df, current_usd_df, constant_usd_df]

for dataframe, name in zip(dataframes, desired_worksheets):
    print(f"{name} DataFrame:")
    print(dataframe.head())
    print()

# Check for missing values in each DataFrame
for dataframe, name in zip(dataframes, desired_worksheets):
    print(f"{name} DataFrame - Missing Values:")
    missing_values = dataframe.isnull().sum()
    print(missing_values)
    print()

# Check for data types and general information about each DataFrame
for dataframe, name in zip(dataframes, desired_worksheets):
    print(f"{name} DataFrame - Info:")
    print(dataframe.info())
    print()

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

for dataframe, name in zip(all_dataframes, all_dataframe_names):
    print(f"Dataframe Info for {name}:\n")
    print(dataframe.info())
    print("\n")

# Rename columns
for dataframe, name in zip(all_dataframes, all_dataframe_names):
    # Create a dictionary to map old column names to new ones
    column_mapping = {
        'Country': 'Country',
        'Currency': 'Currency',
        'Explanation of data': 'Explanation',
        'Comments': 'Comments',
        'Sources of data for last five years, beginning with most recent': 'Sources of data'
    }

    # Rename columns using the dictionary
    dataframe.rename(columns=column_mapping, inplace=True)

    print(f"Columns Renamed for {name}:\n")
    print(dataframe.head())
    print("\n")

# Iterate through all dataframes and their names
for dataframe, name in zip(all_dataframes, all_dataframe_names):
    print(f"Converting Columns to Numeric for {name}:\n")
    
    # Get the columns that are not of type object
    year_columns = [col for col in dataframe.columns if col not in ['Country', 'Currency', 'Explanation of data', 'Comments', 'Sources of data']]
    
    # Convert the selected columns to numeric data type
    dataframe[year_columns] = dataframe[year_columns].apply(pd.to_numeric, errors='coerce')
    
    # Print information about the dataframe after the conversion
    print(f"Dataframe Info for {name}:\n")
    print(dataframe.info())
    print("\n")

# Exploratory Data Analysis (EDA) commences

"""
Global Trends in Military Expenditure

let's identify when military spending increased or dropped in the given years and correlate them with geopolitical events. Below are the years where significant changes (increases or drops) in military expenditure occurred, along with key geopolitical events for those years:

Year: 2003
Event: The Iraq War began in March 2003. The United States led a coalition invasion of Iraq, which led to increased military spending.

Year: 2006
Event: In 2006, there was increased military activity in Iraq and Afghanistan. These conflicts contributed to higher military expenditures.

Year: 2009
Event: The 2008 financial crisis had global economic repercussions. Some countries increased military spending during this period.

Year: 2012
Event: The Syrian Civil War escalated, and there were concerns about the Iranian nuclear program. These events contributed to increased military spending in some regions.

Year: 2016
Event: Various geopolitical tensions, including North Korea's nuclear program and ongoing conflicts in the Middle East, led to increased military expenditures by several countries.

Year: 2019
Event: Some countries reduced military spending in 2019, potentially reflecting changing geopolitical priorities or improved diplomatic relations.

These are simplified examples of how changes in military expenditure can be correlated with geopolitical events. Keep in mind that military spending is influenced by a complex interplay of factors, and individual countries may have unique reasons for their spending patterns.

To visualize these changes and events in the data, we can mark these years on the plot, as below:
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Aggregate global military expenditure over the years
global_spending = constant_usd_exports_df.iloc[:, 1:-3].sum()

# Define the years with significant changes in spending
years_of_interest = [2003, 2006, 2009, 2012, 2016, 2019]

# Find the corresponding data points for those years
interest_points = global_spending[global_spending.index.isin(years_of_interest)]

plt.figure(figsize=(10, 6))
plt.plot(global_spending.index, global_spending.values, marker='o', linestyle='-', label="Expenditure")

# Mark years of interest with larger and more prominent orange dots
plt.scatter(interest_points.index, interest_points.values, color='orange', label="Years of Interest", s=100, edgecolors='black', linewidths=2, zorder=3)

plt.title("Global Military Expenditure Over the Years")
plt.xlabel("Year")
plt.ylabel("Expenditure (Constant USD)")
plt.grid()

# Format the x-axis tick labels as integers
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))

plt.xticks(rotation=45)
plt.legend()
plt.show()
