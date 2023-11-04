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
For meaningful global military expenditure comparison and analysis, it is recommended to use the "constant USD" dataset. Constant USD values adjust for inflation, providing a consistent and standardized measure of military expenditure over time. This dataset allows you to compare military spending across countries and years accurately.

Using the "constant USD" dataset ensures that the values are not affected by inflation, making it suitable for comparative analysis and visualization. It provides a stable basis for understanding trends and making meaningful comparisons.

So, you should share the dataset that contains military expenditure values in "constant USD" for your visualization and analysis.
"""

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

#pip install geopandas

import geopandas as gpd
import matplotlib.pyplot as plt

# Load the world shapefile using the naturalearth_cities dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Specify the aspect ratio
# fig, ax = plt.subplots(subplot_kw={'aspect': 1.0})

# Define regions based on geographical proximity
regions = {
    'Europe': ['Albania', 'Austria', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus',
               'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland',
               'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Montenegro', 'North Macedonia', 'The Netherlands',
               'Norway', 'Poland', 'Portugal', 'Romania', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
               'UK', 'Turkey', 'Russia', 'Ukraine'],

    'Asia': ['India', 'Israel', 'Korea, South', 'Taiwan', 'Pakistan'],

    'Oceania': ['Australia'],

    'North America': ['Canada', 'USA'],

    'South America': ['Brazil'],
}

# Initialize the military expenditure data dictionary
military_expenditure_data = {}

constant_usd_exports_df.fillna(10, inplace=True)

# Add countries to their respective regions in the military_expenditure_data dictionary
for region, countries in regions.items():
    military_expenditure_data[region] = list(countries)

# Iterate through regions and calculate total expenditure for each region
for region, countries in regions.items():
    # Filter the data for countries in the region and fill NaN values with zeros
    region_data = constant_usd_exports_df[constant_usd_exports_df['Country'].isin(countries)]
    region_data = region_data.iloc[:, 1:-3].fillna(0)
    
    # Calculate the total expenditure for the region
    total_expenditure = region_data.sum().sum()
    military_expenditure_data[region] = total_expenditure

# Manually assign 'Industry' to zero expenditure
military_expenditure_data['Industry'] = 0

# Add countries to their respective regions in the world DataFrame
world['Region'] = world['name'].map({country: region for region, countries in regions.items() for country in countries})

# Merge military expenditure data with geometries
world['Expenditure'] = world['Region'].map(military_expenditure_data)

# Plot the choropleth map using the 'YlOrRd' colormap with specified vmin and vmax
# world.boundary.plot()
world.plot(column='Expenditure', legend=True, cmap='viridis', vmin=0, vmax=max(military_expenditure_data.values()))
plt.title('Military Expenditure by Region')
plt.show()

import numpy as np

constant_usd_exports_df.replace(10, np.nan, inplace=True)


# Could've been better had China been there

# Define the countries you want to compare
countries_of_interest = ["India", "USA", "Russia"]

# Initialize an empty dictionary to store the combined military expenditure
combined_data = {"Year": []}

# Initialize empty lists for each country's data
for country in countries_of_interest:
    combined_data[country] = []

# Iterate over the years
for year in constant_usd_exports_df.columns[1:-3]:
    # Check if numeric values are available for all three countries
    if all(
        constant_usd_exports_df[constant_usd_exports_df["Country"] == country][year].notna().all()
        and
        constant_usd_licences_df[constant_usd_licences_df["Country"] == country][year].notna().all()
        for country in countries_of_interest
    ):
        combined_data["Year"].append(year)
        for country in countries_of_interest:
            # Select rows for the country in both datasets
            exports_data = constant_usd_exports_df[constant_usd_exports_df["Country"] == country]
            licences_data = constant_usd_licences_df[constant_usd_licences_df["Country"] == country]

            # Calculate the total military expenditure for the year
            total_expenditure = (
                exports_data[year].sum() + licences_data[year].sum()
            )

            combined_data[country].append(total_expenditure)

# Convert the data dictionary into a DataFrame
combined_df = pd.DataFrame(combined_data)

# Plot a bar chart
combined_df.set_index("Year").plot(kind="bar", figsize=(12, 6))
plt.title("Comparative Military Expenditure")
plt.xlabel("Year")
plt.ylabel("Total Spending (Constant USD)")
plt.grid()
plt.xticks(rotation=45)
plt.legend(title="Country")
plt.show()

"""

The differences in military spending between the USA and Russia from 2002 to 2009 and from 2012 to 2016 can be attributed to a combination of political, economic, and strategic factors. Here are some possible reasons for these differences:

From 2002 to 2009 (USA higher than Russia):

Economic Resources: During this period, the United States had a much larger and stronger economy compared to Russia. The USA's higher GDP allowed it to allocate more funds to military spending.

Global Policymaker: The USA played a significant role as a global superpower and was actively involved in various military operations, including the wars in Afghanistan and Iraq. These operations required substantial military expenditures.

Military Modernization: The United States invested heavily in modernizing its armed forces, which often comes with increased spending. This modernization effort included advancements in technology, procurement of new equipment, and maintaining a large standing military.

From 2012 to 2016 (Closer Spending):

Global Changes: The geopolitical landscape underwent significant changes during this period. The United States started to reduce its military presence in the Middle East, particularly in Iraq and Afghanistan, leading to a decrease in its military expenses.

Russian Military Buildup: Russia, on the other hand, increased its military spending, particularly after its annexation of Crimea in 2014. This resulted in Russia allocating a larger share of its budget to the military.

Economic Challenges: The United States faced economic challenges following the 2008 financial crisis. The subsequent reduction in defense spending, commonly referred to as sequestration, led to a slowdown in the growth of military expenditures.

Strategic Reassessment: The USA and Russia may have reassessed their strategic priorities, leading to adjustments in military budgets. For the USA, the focus shifted towards areas like cybersecurity and technology, while Russia increased investments in its conventional and nuclear capabilities.

Arms Control Agreements: Both countries were signatories to arms control agreements, such as the New START treaty. These agreements can have an impact on the levels of military spending.

"""

# Define the countries you want to compare
countries_of_interest = ["India", "USA"]

# Initialize an empty dictionary to store the combined military expenditure
combined_data = {"Year": []}

# Initialize empty lists for each country's data
for country in countries_of_interest:
    combined_data[country] = []

# Iterate over the years
for year in constant_usd_exports_df.columns[1:-2]:
    # Check if numeric values are available for all three countries
    if all(
        constant_usd_exports_df[constant_usd_exports_df["Country"] == country][year].notna().all()
        and
        constant_usd_licences_df[constant_usd_licences_df["Country"] == country][year].notna().all()
        for country in countries_of_interest
    ):
        combined_data["Year"].append(year)
        for country in countries_of_interest:
            # Select rows for the country in both datasets
            exports_data = constant_usd_exports_df[constant_usd_exports_df["Country"] == country]
            licences_data = constant_usd_licences_df[constant_usd_licences_df["Country"] == country]

            # Calculate the total military expenditure for the year
            total_expenditure = (
                (exports_data[year].sum() + licences_data[year].sum()) / 1000
            )

            combined_data[country].append(total_expenditure)

# Create a DataFrame
combined_df = pd.DataFrame(combined_data)

# Define GDP data for India, USA, and Russia
gdp_data = {
    "India": [510, 582, 652, 772, 875, 1209, 1215, 1377, 1675, 1856, 2042, 2104, 2654],
    "USA": [10600, 10900, 11700, 12400, 13200, 13800, 14400, 14400, 14800, 16200, 16800, 17400, 17900]
}
"""
# Define the military spending data
military_spending_data = {
    #"Year": [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016],
    "United States": [10600, 10900, 11700, 12400, 13200, 13800, 14400, 14400, 14800, 15400, 15700, 16200, 16800, 17400, 17900],
    "Russia": [368, 430, 577, 764, 989, 1299, 1660, 1231, 1524, 2050, 2231, 2297, 2063, 1330, 1282],
    "India": [510, 582, 652, 772, 875, 1209, 1215, 1377, 1675, 1823, 1827, 1856, 2042, 2104, 2654]
}

# Convert the data into a dictionary
gdp_data = {
    "United States": military_spending_data["United States"],
    "Russia": military_spending_data["Russia"],
    "India": military_spending_data["India"],
    #"Year": military_spending_data["Year"]
}
"""

# Update the DataFrame with GDP data
combined_df = combined_df[combined_df['Year'].between(2002, 2016)]  # Select years 2002 to 2016
combined_df = combined_df.reset_index(drop=True)

for country in countries_of_interest:
    combined_df[f'{country}_GDP'] = gdp_data[country]

# Calculate military expenditure as a percentage of GDP
for country in countries_of_interest:
    combined_df[f'{country}_Expenditure_as_Percentage_of_GDP'] = (
        (combined_df[f'{country}'] / combined_df[f'{country}_GDP']) * 100
    )

# Plot trends over different years for all three countries
plt.figure(figsize=(10, 6))

for country in countries_of_interest:
    plt.plot(
        combined_df['Year'],
        combined_df[f'{country}_Expenditure_as_Percentage_of_GDP'],
        label=country,
    )

plt.title('Military Expenditure as a Percentage of GDP (2003-2009)')
plt.xlabel('Year')
plt.ylabel('Expenditure as Percentage of GDP')
plt.legend()
plt.grid(True)

# Format the y-axis as percentages
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))

plt.show()

"""
During the period from 2002 to 2016, the military expenditures as a percentage of GDP for India and the United States varied for a combination of historical, geopolitical, and economic reasons:

India:

Historical Factors: India's military spending as a percentage of GDP remained relatively low during this period, which can be attributed to its historical focus on non-alignment during the Cold War and its commitment to peaceful coexistence. India traditionally prioritized socio-economic development over military expansion.

Geopolitical Factors: India's primary focus during this period was regional security, with a particular emphasis on border disputes with Pakistan and China. While the Indian defense budget increased, it was not a significant proportion of GDP. India's policy was to maintain a credible minimum deterrence, which allowed for a more conservative approach to defense spending.

Economic Factors: India experienced steady economic growth during these years. A growing economy allowed for increased government revenue and investment in other sectors, such as infrastructure and social programs. As a result, military spending as a percentage of GDP remained low.

United States:

Historical Factors: The United States has a long history of being a global military power. It was engaged in several military conflicts, including the War on Terror and the Iraq War, which significantly increased military spending.

Geopolitical Factors: The United States' role as a global superpower led to substantial defense commitments around the world. It maintained a global military presence, including military bases in various countries. Furthermore, it was actively involved in conflicts in Iraq and Afghanistan.

Economic Factors: The U.S. had the world's largest economy and defense budget. It could afford to allocate a substantial portion of its GDP to defense spending. The defense industry also played a significant role in the U.S. economy, with strong political and economic incentives for high levels of military expenditure.

In summary, India's lower military spending as a percentage of GDP during 2002-2016 was primarily influenced by its historical approach to non-alignment, regional security priorities, and a focus on economic development. The United States, on the other hand, had a more interventionist global military presence and higher defense expenditures due to its historical role as a superpower, its global commitments, and its strong economy. These factors led to significant differences in military spending as a percentage of GDP between the two countries during this period.
"""

from statsmodels.tsa.arima.model import ARIMA

# Load and preprocess the data for selected countries (similar to previous code)
# Define the countries you want to compare
countries_of_interest = ["India", "Germany"]

# Initialize an empty dictionary to store the combined military expenditure
combined_data = {"Year": []}

# Initialize empty lists for each country's data
for country in countries_of_interest:
    combined_data[country] = []

# Iterate over the years
for year in constant_usd_exports_df.columns[1:-2]:
    # Check if numeric values are available for all three countries
    if all(
        constant_usd_exports_df[constant_usd_exports_df["Country"] == country][year].notna().all()
        and
        constant_usd_licences_df[constant_usd_licences_df["Country"] == country][year].notna().all()
        for country in countries_of_interest
    ):
        combined_data["Year"].append(year)
        for country in countries_of_interest:
            # Select rows for the country in both datasets
            exports_data = constant_usd_exports_df[constant_usd_exports_df["Country"] == country]
            licences_data = constant_usd_licences_df[constant_usd_licences_df["Country"] == country]

            # Calculate the total military expenditure for the year
            total_expenditure = (
                (exports_data[year].sum() + licences_data[year].sum()) / 1000
            )

            combined_data[country].append(total_expenditure)

# Create a DataFrame
combined_df = pd.DataFrame(combined_data)

# Feature Engineering: Prepare time-series data
combined_df = combined_df.set_index("Year").stack().reset_index()
combined_df.columns = ["Year", "Country", "Expenditure"]

# Define the selected countries for forecasting, including India
selected_countries = ['India', 'Germany']

# Initialize a dictionary to store forecasted data
forecasted_data = {}

# Initialize a dictionary to store each country's historical data
historical_data = {}

# Time-Series Forecasting for each selected country
for country in selected_countries:
    # Filter data for the current country
    country_data = combined_df[combined_df['Country'] == country]

    # Convert 'Year' to datetime
    country_data['Year'] = pd.to_datetime(country_data['Year'], format='%Y')

    # Set 'Year' as the index
    country_data.set_index('Year', inplace=True)

    # Store historical data for the country
    historical_data[country] = country_data

    # Train an ARIMA model (you may need to fine-tune hyperparameters)
    model = ARIMA(country_data['Expenditure'], order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast future values for 18 years into the future
    forecasted = model_fit.forecast(steps=18)
    forecasted_years = pd.date_range(start=country_data.index.max(), periods=18, freq='Y')

    # Store the forecasted data in the dictionary
    forecasted_data[country] = pd.DataFrame({'Year': forecasted_years, 'Expenditure': forecasted})

# Visualization: Plot historical and forecasted data for all selected countries
plt.figure(figsize=(12, 6))

# Convert 'Year' to datetime with December 31st for all years
combined_df['Year'] = pd.to_datetime(combined_df['Year'].astype(str) + '-12-31')
combined_df.set_index('Year', inplace=True)

for country, forecasted_df in forecasted_data.items():
    plt.plot(
        historical_data[country].index,  # Access the datetime index
        historical_data[country]["Expenditure"],  # Access the "Expenditure" column
        label=f'{country} (Historical)'
    )

    plt.plot(
        forecasted_df['Year'],
        forecasted_df['Expenditure'],
        linestyle='--',
        marker='o',
        label=f'{country} (Forecast)'
    )

plt.title('Historical and Forecasted Military Expenditure (Constant USD)')
plt.xlabel('Year')
plt.ylabel('Expenditure (Constant USD)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

plt.show()

"""
analysis of the trends in Germany's and India's military expenditures based on historical and geopolitical events:

Germany's Military Expenditure:

Surge in 2008: Germany's military expenditure experienced a significant surge in 2008. This aligns with the timeline of international events such as the NATO-led military campaign in Afghanistan. Germany increased its military involvement and financial contributions to international peacekeeping missions, which required a higher defense budget.

Decline Post-2008: After the peak in 2008, Germany's defense spending began to decline. This could be attributed to a reassessment of Germany's strategic priorities. Following the financial crisis of 2008, many countries, including Germany, implemented austerity measures, which likely affected defense budgets.

Temporary Rise in 2013: The temporary rise in 2013 could be related to a changing geopolitical landscape. Tensions with Russia over Ukraine and other security challenges in Europe may have prompted Germany to allocate more resources to defense. This increase was consistent with NATO's call for member states to enhance their military capabilities.

Moderation Post-2013: In the years following 2013, Germany's military expenditure remained relatively stable and even decreased. This suggests that the temporary increase in 2013 might have been driven by specific geopolitical events or policy changes that were not sustained in the long term.

India's Military Expenditure:

Steady Growth Pre-2016: India's military expenditure remained relatively stable up to 2016. This period was characterized by ongoing border tensions with Pakistan, the modernization of the armed forces, and persistent security challenges in the region.

Rapid Increase Post-2016: The subsequent significant increase in India's military expenditure from 2016 onwards aligns with a notable shift in India's geopolitical stance. Several factors contribute to this trend, including increasing border tensions with China, ongoing concerns about Pakistan-based terrorism, and India's aspiration to enhance its regional and global influence. This upward trajectory also reflects India's efforts to modernize its military capabilities and infrastructure.

In summary, Germany's military expenditure trends can be linked to international peacekeeping missions, fiscal considerations, and shifts in security priorities. On the other hand, India's trends reflect its evolving geopolitical challenges, regional security concerns, and a commitment to strengthening its defense capabilities. These interpretations are based on historical patterns and geopolitical knowledge, but it's essential to consult specific historical and political sources for a more comprehensive analysis.
"""

#---------------------------------------------------#


# Specify the file path
file_path = r'D:\Projects\datathon23\datasets\Total_Arms_Sales.xlsx'

# Read data from the Excel file
data = pd.read_excel(file_path, sheet_name="Sheet1", skiprows=[0, 1, 2, 6, 9])

# Remove rows 0 and 1
data = data.drop([0, 1])

# Reset the index to start from 0
data = data.reset_index(drop=True)

import matplotlib.pyplot as plt

# Data
years = data.columns[1:-1].astype(float)  # Extract years as floats
total_sales = data.iloc[0, 1:-1].astype(float)
percentage_change = data.iloc[1, 1:-1].astype(float)

# Create subplots
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot total arms sales on the primary y-axis
ax1.set_xlabel('Year')
ax1.set_ylabel('Total Arms Sales (Constant 2021 USD Billion)', color='tab:blue')
ax1.plot(years, total_sales, color='tab:blue', label='Total Sales')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot percentage change on the secondary y-axis
ax2.set_ylabel('Percentage Change', color='tab:orange')
ax2.bar(years, percentage_change, color='tab:orange', label='Percentage Change', alpha=0.5)
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Set labels and title
plt.title('Total Arms Sales and Percentage Change Over Years (2002-2021)')
plt.xlabel('Year')

# Set tick positions and labels for years with decimals every two years
xticks = [int(year) if year.is_integer() and int(year) % 2 == 0 else '' for year in years]
plt.xticks(years, xticks)

# Add a legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Display the plot
plt.show()

"""
The data represents total arms sales in constant 2021 USD billion for the top 100 arms companies globally from 2002 to 2021, along with the percentage change each year. Let's relate this data to significant geopolitical situations and events during this period:

2002-2003 - Post-9/11 Conflict: The increase in arms sales between 2002 and 2003 may be attributed to the United States' response to the 9/11 terrorist attacks. The U.S. led the global war on terror, resulting in increased defense spending.

2003-2005 - Iraq War: The arms sales continued to rise as the Iraq War began in 2003. This conflict led to high military expenditures, primarily by the U.S. and its allies.

2008 - Global Financial Crisis: In 2008, there was a significant peak in arms sales. This was the year of the global financial crisis. Paradoxically, arms sales increased during economic downturns as countries invested in defense.

2013-2014 - Conflict in Ukraine: The increase in arms sales during this period coincides with the conflict in Ukraine, including the annexation of Crimea by Russia. It led to a surge in defense spending by NATO members.

2015-2016 - Syrian Civil War: The arms sales continued to rise, possibly due to the ongoing Syrian Civil War. Multiple countries supported various factions, leading to increased arms trade.

2020-2021 - COVID-19 Pandemic: The substantial spike in arms sales in 2020-2021 might be related to the COVID-19 pandemic. Countries may have increased their defense spending due to geopolitical uncertainties stemming from the pandemic.

Overall Trends: The overall trend of increasing arms sales reflects geopolitical tensions, regional conflicts, and the modernization of armed forces globally. The intermittent decreases may represent efforts to reduce military expenditure during periods of relative peace.

The percentage changes highlight the year-to-year variations. The significant increase in 2014 is particularly noticeable, possibly related to intensified conflicts in the Middle East and Eastern Europe. The data shows how political events and crises can influence arms sales and military expenditure.
"""

#-----------------------------------------------------------------#

import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Top_100_Arms-Producing.xlsx')

# Read the data for the year 2021 and skip the first three rows
df_2021 = pd.read_excel(xls, '2021', skiprows=3)

# Create a dictionary to map the old column names to the new names
column_name_mapping = {
    'Country (d)': 'Country',
    'Company (c) ': 'Company'
}

# Rename columns based on the mapping
df_2021 = df_2021.rename(columns=column_name_mapping)

# Group data by country and company, and sum the sales
grouped_data = df_2021.groupby(['Country', 'Company'])['Arms Sales (2021)'].sum().unstack(fill_value=0)

# Sort companies by total sales and select the top 10
top_10_companies = grouped_data.sum().nlargest(10).index

# Assign unique colors to all companies
colors = plt.cm.get_cmap('tab20', len(grouped_data.columns))

# Create a stacked bar chart for the year 2021
fig, ax = plt.subplots(figsize=(12, 6))
bottom = np.zeros(len(grouped_data))
company_colors = {}

for company in grouped_data.columns:
    color = colors(len(company_colors))
    company_colors[company] = color
    plt.bar(grouped_data.index, grouped_data[company], bottom=bottom, label=company, color=color)
    bottom += grouped_data[company]

# Add a legend with company names and their respective colors
legend_labels = [plt.Line2D([0], [0], color=company_colors[company], label=company) for company in top_10_companies]
plt.legend(handles=legend_labels, title='Company')

plt.xlabel('Country')
plt.ylabel('Arms Sales (in millions of US$)')
plt.xticks(rotation=45)
plt.title('Arms Sales by Companies and Countries - 2021')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Top_100_Arms-Producing.xlsx')

# Dictionary to store historical sales data
sales_data = {}

# Possible company column names
possible_company_columns = ['Company (c)', 'Company (c) ', ' Company (c)', ' Company (c)']

# Iterate through worksheets (years)
for sheet_name in xls.sheet_names:
    # Remove leading and trailing spaces from the worksheet name
    sheet_name = sheet_name.strip()

    # Read the data for the current worksheet and skip the first three rows
    df = pd.read_excel(xls, sheet_name, skiprows=3)
    
    # Identify the company column based on various possible column names
    company_column = None
    for col_name in possible_company_columns:
        if col_name in df.columns:
            company_column = col_name
            break

    # Check if an arms sales column is present
    arms_sales_column = None
    for col_name in df.columns:
        if col_name.strip().startswith('Arms Sales'):
            arms_sales_column = col_name
            break
    
    if company_column is not None and arms_sales_column is not None:
        # Iterate through the rows of the dataframe
        for index, row in df.iterrows():
            company = str(row[company_column]).strip()
            year = int(sheet_name)
            arms_sales = row[arms_sales_column]
            if company not in sales_data:
                sales_data[company] = {'years': [], 'sales': []}
        
            sales_data[company]['years'].append(year)
            sales_data[company]['sales'].append(arms_sales)

# Filter companies with data for all years from 2002 to 2021
selected_companies = {}
for company, data in sales_data.items():
    years = data['years']
    if len(years) == 20 and min(years) == 2002 and max(years) == 2021:
        selected_companies[company] = data

# Create a visualization of historical sales for the top companies
plt.figure(figsize=(12, 6))
count = 0  # Initialize a count variable
for company, data in selected_companies.items():
    # Break the loop if more than 10 iterations have been performed
    if count >= 5:
        break
    
    # Prepare your data for model training
    historical_years = np.array(data['years']).reshape(-1, 1)
    historical_sales = np.array(data['sales'])

    # Train a linear regression model
    model = LinearRegression()
    model.fit(historical_years, historical_sales)

    # Predict future sales for the next 10 years
    future_years = np.array(range(2022, 2032)).reshape(-1, 1)
    predicted_sales = model.predict(future_years)

    # Plot historical sales with solid lines
    plt.plot(data['years'], data['sales'], label=f'{company} (Historical)')

    # Plot predicted sales with dotted lines
    plt.plot(future_years, predicted_sales, linestyle='--', label=f'{company} (Predicted)')
    
    # Increment the count
    count += 1

plt.xlabel('Year')
plt.ylabel('Sales')
plt.title('Historical and Predicted Sales for Selected Companies (2002-2031)')
plt.legend()
plt.show()

#---------------------------------------------------------------#

import pandas as pd

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Read the data for the year 2021 and skip the first three rows
df = pd.read_excel(xls, sheet_name="Regional totals", skiprows=14)

# Desrcriptive Statistics

# Select the columns with numeric data (from 1950 to 2019)
numeric_columns = df.columns[1:-2]

# Convert the selected columns to numeric (ignoring errors for non-numeric and NaN values)
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Calculate mean, median, and standard deviation for each row (region) while ignoring NaN values
df['Mean'] = df[numeric_columns].mean(axis=1, skipna=True)
df['Median'] = df[numeric_columns].median(axis=1, skipna=True)
df['Standard Deviation'] = df[numeric_columns].std(axis=1, skipna=True)

# Select the columns of interest (Region and the calculated statistics)
summary_stats = df[['Region', 'Mean', 'Median', 'Standard Deviation']]

# Display the summary statistics
print(summary_stats)


import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["2019 (current prices)", "Omitted countries"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows and columns
df = pd.read_excel(xls, sheet_name="Regional totals", skiprows=14, usecols=lambda x: x not in columns_to_skip)

# Remove the last (unnamed) column
df = df.iloc[:, :-1]  # This selects all columns except the last one

# Select a region of interest, e.g., 'World total (excluding Iraq)'
region_data = df[df['Region'] == 'World total (including Iraq)']

# Define the numeric columns (years) for the time series
numeric_columns = region_data.columns[1:]

# Convert the selected columns to numeric (ignoring errors for non-numeric and NaN values)
region_data[numeric_columns] = region_data[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Create a time series with the data
ts = region_data.iloc[0, 1:].fillna(0).values  # Fill missing values with zeros

# Set the frequency of the time series to 'A' (annual)
ts = pd.Series(ts, index=pd.date_range(start='1950-01-01', periods=len(ts), freq='A'))

# Perform time series decomposition (trend, seasonal, and residual)
decomposition = sm.tsa.seasonal_decompose(ts, model='additive')

# Plot the original time series, trend, seasonality, and residuals
plt.figure(figsize=(12, 6))
plt.subplot(411)
plt.title('Time Series Analysis for Military Expenditure by the World (including Iraq)')
plt.plot(ts, label='Original', color='blue')
plt.legend()

plt.subplot(412)
plt.title('Trend')
plt.plot(decomposition.trend, label='Trend', color='red')
plt.legend()

plt.subplot(413)
plt.title('Seasonality')
plt.plot(decomposition.seasonal, label='Seasonal', color='green')
plt.legend()

plt.subplot(414)
plt.title('Residuals')
plt.plot(decomposition.resid, label='Residuals', color='purple')
plt.legend()

plt.tight_layout()
plt.show()

"""
If the seasonality and residuals are straight lines parallel to the x-axis, and the trend curve is the same as the original time series curve, it suggests that there might be an issue with the decomposition or the data you're using for decomposition. In a proper time series decomposition, you would typically expect:

Original Time Series: This represents the actual data, and the pattern in the original time series should be a combination of trend, seasonality, and residuals. It's not unusual for the original time series to exhibit trends, seasonality, and variations.

Trend: The trend component should capture the long-term, systematic variation in the data. It may go up or down over time, indicating a significant and sustained change in the data. If the trend curve is identical to the original time series, it could indicate that the decomposition process did not effectively separate the trend component.

Seasonality: Seasonality should capture periodic, repeating patterns in the data. If the seasonal component is a straight line parallel to the x-axis, it may suggest that there is no significant seasonal pattern in the data, or there could be issues with the decomposition.

Residuals: The residuals represent the unexplained or random variation in the data after removing the trend and seasonality. A straight line for residuals may indicate that the model has captured most of the variation, and what remains is relatively constant.

Here are some possible explanations for the observations you described:

The data may not contain strong seasonal patterns.
The decomposition model may not be suitable for this dataset.
There might be errors or issues in the implementation of the decomposition process.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["2019 (current prices)", "Omitted countries"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows and columns
df = pd.read_excel(xls, sheet_name="Regional totals", skiprows=14, usecols=lambda x: x not in columns_to_skip)

# Remove the last (unnamed) column
df = df.iloc[:, :-1]  # This selects all columns except the last one

# Pivot the DataFrame so that 'Region' becomes the index
df_pivoted = df.set_index('Region')

# Transpose the DataFrame to have years as the index
df_pivoted = df_pivoted.T

# Convert the data to numeric, replacing non-numeric values with NaN
df_pivoted = df_pivoted.apply(pd.to_numeric, errors='coerce')

# Calculate the correlation matrix
correlation_matrix = df_pivoted.corr()

# Create a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title("Correlation Heatmap of Military Expenditure by Region")
plt.show()

# Threshold for considering correlations
correlation_threshold = 0.8

# Create a list to store textual explanations
explanations = []

# Iterate over the columns of the correlation matrix
for col in correlation_matrix.columns:
    for idx, value in correlation_matrix[col].items():
        if col != idx and abs(value) >= correlation_threshold:
            explanation = f"The military spending of '{col}' is "
            if value > 0:
                explanation += f"positively correlated with '{idx}'"
            else:
                explanation += f"negatively correlated with '{idx}'"
            explanation += f" (Correlation: {value:.2f})"
            explanations.append(explanation)

# Print the explanations
for explanation in explanations:
    print(explanation)
    
    

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["2019 (current prices)", "Omitted countries"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows and columns
df = pd.read_excel(xls, sheet_name="Regional totals", skiprows=14, usecols=lambda x: x not in columns_to_skip)

# Extract the columns with military spending data (years)
military_spending_data = df.iloc[:, 1:]

# Convert feature names (column names) to strings
military_spending_data.columns = military_spending_data.columns.astype(str)

# Replace non-numeric values with NaN
military_spending_data = military_spending_data.apply(pd.to_numeric, errors='coerce')

# Perform data preprocessing, if necessary (e.g., handling missing values, scaling)

# Standardize the data (important for K-Means)
scaler = StandardScaler()
military_spending_data_scaled = scaler.fit_transform(military_spending_data)

from sklearn.impute import SimpleImputer

# Create a SimpleImputer to impute NaN values with the mean of each column
imputer = SimpleImputer(strategy='mean')

# Impute the NaN values
military_spending_data_imputed = imputer.fit_transform(military_spending_data_scaled)

# Determine the optimal number of clusters using the Elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(military_spending_data_imputed)
    wcss.append(kmeans.inertia_)

# Plot the Elbow method results
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')  # Within-Cluster Sum of Squares
plt.show()

# Choose an appropriate number of clusters based on the Elbow method results
# For example, you can set n_clusters = 3 if the 'elbow' of the plot is around 3

# Perform K-Means clustering
n_clusters = 3  # You can change this based on the Elbow method result
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
cluster_labels = kmeans.fit_predict(military_spending_data_scaled)

# Add the cluster labels to the DataFrame
df['Cluster'] = cluster_labels

# Now, df contains the original data with an additional 'Cluster' column indicating the cluster for each region
# You can analyze and visualize the clusters as needed

"""
In K-Means clustering, the Within-Cluster-Sum-of-Squares (WCSS) is a measure of the variability or dispersion of data points within the clusters. It is an important metric used to determine the optimal number of clusters in K-Means.

When you plot the WCSS for different values of k (the number of clusters), you often observe a curve that starts high and decreases as k increases, forming an "elbow" shape. The "elbow" point in the curve is typically where you should choose the number of clusters.

At the beginning of the curve (small k values), adding more clusters reduces the WCSS significantly. This is because each data point is closer to the centroids, leading to smaller within-cluster variations.

As you increase k, the reduction in WCSS becomes less pronounced, and the curve starts to bend. The "elbow" point is where the rate of reduction sharply changes or levels off. This point represents a good trade-off between the number of clusters and the compactness of the clusters.

Selecting the number of clusters at the "elbow" point is a common heuristic for determining the optimal number of clusters. However, the choice of the exact number of clusters can still be somewhat subjective and may require domain knowledge and additional analysis.

So, when you see a curve with an "elbow" shape, it suggests that the point where the curve starts to bend is a reasonable choice for the number of clusters that effectively represent the underlying structure of your data.
"""

optimal_k = 3  # Replace with the number of clusters you've determined

kmeans = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=300, n_init=10, random_state=0)
kmeans.fit(military_spending_data_imputed)

# Get cluster labels for each data point
cluster_labels = kmeans.predict(military_spending_data_imputed)

# Assign cluster labels to your DataFrame
df['Cluster'] = cluster_labels

cluster_0_data = df[df['Cluster'] == 0]
cluster_1_data = df[df['Cluster'] == 1]
cluster_2_data = df[df['Cluster'] == 2]

# Replace non-numeric values with NaN
df = df.replace('. .', np.nan)

# Now, create a scatter plot for all clusters
cluster_labels = [0, 1, 2]  # Replace with the cluster labels you have
colors = ['red', 'blue', 'green']  # You can choose different colors for each cluster
labels = ['Americas', 'Rest of the World', 'World Total']

plt.figure(figsize=(10, 6))

for i, cluster_label in enumerate(cluster_labels):
    cluster_data = df[df['Cluster'] == cluster_label]
    years = df.columns[1:-2]  # Assuming the year columns are from the second column to the third-to-last column
    spending_values = cluster_data.iloc[0, 1:-2]  # Assuming you want to plot the first row of each cluster
    plt.scatter(years, spending_values, label=f'Cluster {cluster_label}: {labels[i]}', color=colors[i])

plt.title('Cluster Demarcation')
plt.xlabel('Years')
plt.ylabel('Military Spending')
plt.legend()
plt.show()



import pandas as pd
import numpy as np

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Define a list of columns to skip
columns_to_skip = ["2019 (current prices)", "Omitted countries"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows and columns
df = pd.read_excel(xls, sheet_name="Regional totals", skiprows=14, usecols=lambda x: x not in columns_to_skip)

# Remove the rightmost column
df = df.iloc[:, :-1]

# Extract the columns with military spending data (years)
military_spending_data = df.iloc[:, 1:]

# Convert feature names (column names) to strings
military_spending_data.columns = military_spending_data.columns.astype(str)

# Replace non-numeric values with NaN
military_spending_data = military_spending_data.apply(pd.to_numeric, errors='coerce')

# Perform anomaly detection using Z-scores
# Define a threshold for anomaly detection (e.g., 2.0 for a 95% confidence interval)
threshold = 2.5

# Calculate the mean and standard deviation for each year
mean = military_spending_data.mean()
std = military_spending_data.std()

# Calculate Z-scores for each data point
z_scores = (military_spending_data - mean) / std

# Identify anomalies based on the threshold
anomalies = z_scores > threshold

# Print the index where anomalies are detected
anomalous_regions = anomalies.index[anomalies.any(axis=1)]

# Print the anomalous regions
print("Anomalous Regions:", anomalous_regions)

anomalous_region_names = df['Region'].iloc[anomalous_regions]
print("Anomalous Region Names:", anomalous_region_names)

"""
Rationale and Explanation:

Z-Scores: Z-scores are a measure of how far away a particular data point is from the mean of the data in terms of standard deviations. In this context, Z-scores are used to identify regions with military spending that significantly deviates from the mean. A high absolute Z-score indicates an extreme deviation.

Threshold Value: The threshold value is a critical parameter in anomaly detection. It defines the cutoff point for what is considered an anomaly. In your code, anomalies are identified when the absolute Z-score is greater than this threshold.

Anomaly Detection: Anomaly detection is the process of identifying data points that are significantly different from the majority of the data. It's valuable for discovering unusual patterns or outliers in your data. In this case, you're looking for regions with military spending that are exceptionally high or low compared to the rest.
"""

import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the Z-scores for each region
for i in range(len(z_scores.columns)):
    ax.bar(z_scores.index, z_scores.iloc[:, i], align='center', alpha=0.7)

# Highlight regions that cross the threshold
anomalous_regions_indices = [i for i, region in enumerate(z_scores.index) if region in anomalous_regions]
for i in anomalous_regions_indices:
    ax.bar(z_scores.index, z_scores.iloc[:, i], color='red', alpha=0.7, label=f'Region {i}')

# Add a horizontal dotted line at the threshold
ax.axhline(y=threshold, color='black', linestyle='--', label='Threshold')

# Rotate x-axis labels for better readability
plt.xticks(rotation=90)

# Set labels and title
ax.set_xlabel('Regions')
ax.set_ylabel('Z-Scores')
ax.set_title('Z-Scores for Military Spending Anomaly Detection')

# Adjust the legend to avoid duplicate labels
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# Display the plot
plt.show()



import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["Notes", "2019 Current"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows and columns
df = pd.read_excel(xls, sheet_name="Constant (2018) USD", skiprows=5, usecols=lambda x: x not in columns_to_skip)

# Drop the second column from the DataFrame
df = df.drop(df.columns[1], axis=1)

# Extract the columns with military spending data (years)
military_spending_data = df.iloc[:, 1:]

# Convert feature names (column names) to strings
military_spending_data.columns = military_spending_data.columns.astype(str)

# Replace non-numeric values with NaN
military_spending_data = military_spending_data.apply(pd.to_numeric, errors='coerce')

# Perform data preprocessing, if necessary (e.g., handling missing values, scaling)

# Standardize the data (important for K-Means)
scaler = StandardScaler()
military_spending_data_scaled = scaler.fit_transform(military_spending_data)

from sklearn.impute import SimpleImputer

# Create a SimpleImputer to impute NaN values with the mean of each column
imputer = SimpleImputer(strategy='mean')

# Impute the NaN values
military_spending_data_imputed = imputer.fit_transform(military_spending_data_scaled)

# Determine the optimal number of clusters using the Elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(military_spending_data_imputed)
    wcss.append(kmeans.inertia_)

# Plot the Elbow method results
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')  # Within-Cluster Sum of Squares
plt.show()

# Choose an appropriate number of clusters based on the Elbow method results
# For example, you can set n_clusters = 3 if the 'elbow' of the plot is around 3

# Perform K-Means clustering
n_clusters = 2  # You can change this based on the Elbow method result

# Create an imputer that replaces NaNs with the mean value of the column
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

# Perform imputation on the scaled data
military_spending_data_scaled_imputed = imputer.fit_transform(military_spending_data_scaled)

# Perform K-Means clustering
n_clusters = 2  # You can change this based on the Elbow method result
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
cluster_labels = kmeans.fit_predict(military_spending_data_scaled_imputed)


# Add the cluster labels to the DataFrame
df['Cluster'] = cluster_labels

# Now, df contains the original data with an additional 'Cluster' column indicating the cluster for each region
# You can analyze and visualize the clusters as needed

"""
In K-Means clustering, the Within-Cluster-Sum-of-Squares (WCSS) is a measure of the variability or dispersion of data points within the clusters. It is an important metric used to determine the optimal number of clusters in K-Means.

When you plot the WCSS for different values of k (the number of clusters), you often observe a curve that starts high and decreases as k increases, forming an "elbow" shape. The "elbow" point in the curve is typically where you should choose the number of clusters.

At the beginning of the curve (small k values), adding more clusters reduces the WCSS significantly. This is because each data point is closer to the centroids, leading to smaller within-cluster variations.

As you increase k, the reduction in WCSS becomes less pronounced, and the curve starts to bend. The "elbow" point is where the rate of reduction sharply changes or levels off. This point represents a good trade-off between the number of clusters and the compactness of the clusters.

Selecting the number of clusters at the "elbow" point is a common heuristic for determining the optimal number of clusters. However, the choice of the exact number of clusters can still be somewhat subjective and may require domain knowledge and additional analysis.

So, when you see a curve with an "elbow" shape, it suggests that the point where the curve starts to bend is a reasonable choice for the number of clusters that effectively represent the underlying structure of your data.
"""

cluster_0_data = df[df['Cluster'] == 0]
cluster_1_data = df[df['Cluster'] == 1]

# Replace non-numeric values with NaN
df = df.replace('. .', np.nan)

# Now, create a scatter plot for all clusters
cluster_labels = [0, 1]  # Replace with the cluster labels you have
colors = ['red', 'blue']  # You can choose different colors for each cluster
labels = ['USA', 'Rest of the World']

plt.figure(figsize=(10, 6))

for i, cluster_label in enumerate(cluster_labels):
    cluster_data = df[df['Cluster'] == cluster_label]
    years = df.columns[1:-1]  # Assuming the year columns are from the second column to the third-to-last column
    spending_values = cluster_data.iloc[0, 1:-1]  # Assuming you want to plot the first row of each cluster
    # Set the point size. Use a larger size for the cluster with fewer points.
    point_size = 10000 if len(cluster_data) < 2 else 20
    plt.scatter(years, spending_values, label=f'Cluster {cluster_label}: {labels[i]}', color=colors[i])

plt.title('Cluster Demarcation')
plt.xlabel('Years')
plt.ylabel('Military Spending')
plt.legend()
plt.show()



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the Excel file with multiple worksheets
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["Notes"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows, columns, and the last 8 rows
df = pd.read_excel(xls, sheet_name="Share of GDP", skiprows=5, usecols=lambda x: x not in columns_to_skip, skipfooter=8)

df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Extract data for India and USA
india_data = df[df['Country'] == 'India']
usa_data = df[df['Country'] == 'USA']

# Create a plot for India and USA
plt.figure(figsize=(12, 6))
plt.plot(india_data.columns[1:], india_data.values[0][1:], label='India', marker='o')
plt.plot(usa_data.columns[1:], usa_data.values[0][1:], label='USA', marker='o')
plt.xlabel('Year')
plt.ylabel('Military Expenditure (% of GDP)')
plt.title('Military Expenditure of India and USA (1949-2019)')
plt.legend()
plt.grid(True)
plt.show()



# plot health expenditure and military expenditure (per capita) with the population in the background as bar graph
import pandas as pd
import numpy as np

# Load the excel file for per capita military expenditure by country data
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["Notes"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows, columns, and the last 8 rows
df_military = pd.read_excel(xls, sheet_name="Per capita", skiprows=6, usecols=lambda x: x not in columns_to_skip, skipfooter=7)

# Replace non-numeric values with NaN
df_military = df_military.replace('. .', np.nan)

df_military.iloc[:, 1:] = df_military.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Load the excel file for per capita military expenditure by country data
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\external\WHO_Global_Health_Expenditure.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["Country Code", "Indicator Name", "Indicator Code"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows, columns, and the last 8 rows
df_health = pd.read_excel(xls, sheet_name="Data", skiprows=3, usecols=lambda x: x not in columns_to_skip, skipfooter=2)

# Discard columns between 1960 and 2000
df_health = df_health.drop(df_health.loc[:, '1960':'2000'], axis=1)

# Discard the rightmost 2 columns
df_health = df_health.iloc[:, :-2]

# Load the excel file for per capita military expenditure by country data
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\external\IMF_World_Economic_Outlook_Database.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["Subject Notes", "Units", "Scale", "Country/Series-specific Notes"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows, columns, and the last 8 rows
df_population = pd.read_excel(xls, sheet_name="IMF_World_Economic_Outlook_Data", usecols=lambda x: x not in columns_to_skip, skipfooter=2)

# Filter the rows where "Subject Descriptor" is "Population"
df_population = df_population[df_population["Subject Descriptor"] == "Population"]

# Drop the "Subject Descriptor" column
df_population = df_population.drop("Subject Descriptor", axis=1)

# Discard the rightmost 1 columns
df_population = df_population.iloc[:, :-1]

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Specify the countries you want to plot
countries = ["China", "Afghanistan", "Bangladesh", "India", "Nepal", "Pakistan", "Sri Lanka", "Myanmar"]

# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 6))

# Create a color map for distinguishing lines of different countries
colors = plt.cm.get_cmap("tab10", len(countries))

# Create lists to store legend handles and labels
legend_handles = []
legend_labels = []

# Plot per capita health expenditure data for each country
for i, country in enumerate(countries):
    if country in df_health["Country Name"].values:
        health_data = df_health[df_health["Country Name"] == country].values[0][1:]
        years = df_health.columns[1:].astype(int)  # Extract years as integers
        line, = ax1.plot(years, health_data, label=country + " (Health)", color=colors(i))
        if country == "India":
            line.set_linewidth(5)  # Increase line width for India
        legend_handles.append(line)
        legend_labels.append("Health (Solid) - " + country)

# Create a second y-axis for per capita military expenditure
ax2 = ax1.twinx()

for i, country in enumerate(countries):
    if country in df_military["Country"].values:
        military_data = df_military[df_military["Country"] == country].values[0][13:33]  # Select the relevant years
        line, = ax2.plot(years, military_data, label=country + " (Military)", linestyle="--", color=colors(i))
        if country == "India":
            line.set_linewidth(5)  # Increase line width for India
        legend_handles.append(line)
        legend_labels.append("Military (Dotted) - " + country)

# Create a third y-axis for population
ax3 = ax1.twinx()

for i, country in enumerate(countries):
    if country in df_population["Country"].values:
        population_data = df_population[df_population["Country"] == country].values[0][13:33]  # Select the relevant years
        line, = ax3.plot(years, population_data, label=country + " (Population)", linestyle="-.", color=colors(i))
        if country == "India":
            line.set_linewidth(5)  # Increase line width for India
        legend_handles.append(line)
        legend_labels.append("Population (Dashed) - " + country)

# Customize the plot
ax1.set_xlabel("Year")
ax1.set_ylabel("Per Capita Military/Health Expenditure", labelpad=15)
ax2.set_ylabel("")  # Remove right y-axis label

# Show the legend with custom entries for different line styles
ax1.legend(legend_handles, legend_labels, loc="upper left")

# Remove right y-axis ticks and labels (except for population)
ax2.set_yticks([])

ax2.set_ylabel("Population", labelpad=40)
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))  # Set the x-axis to display integers only

plt.title("Per Capita Military/Health Expenditure and Population by Country")

# Show the plot
plt.tight_layout()
plt.show()





import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the excel file for per capita military expenditure by country data
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\external\IMF_World_Economic_Outlook_Database.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["Subject Notes", "Units", "Scale", "Country/Series-specific Notes"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows, columns, and the last 8 rows
df_inflation = pd.read_excel(xls, sheet_name="IMF_World_Economic_Outlook_Data", usecols=lambda x: x not in columns_to_skip, skipfooter=2)

# Filter the rows where "Subject Descriptor" is "Inflation, average consumer prices"
df_inflation = df_inflation[df_inflation["Subject Descriptor"] == "Inflation, average consumer prices"]

# Drop the "Subject Descriptor" column
df_inflation = df_inflation.drop("Subject Descriptor", axis=1)

# Discard the rightmost 1 columns
df_inflation = df_inflation.iloc[:, :-1]  # Exclude the first and last columns

# Load the excel file for per capita military expenditure by country data
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\external\IMF_World_Economic_Outlook_Database.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["Subject Notes", "Units", "Scale", "Country/Series-specific Notes"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows, columns, and the last 8 rows
df_unemployment = pd.read_excel(xls, sheet_name="IMF_World_Economic_Outlook_Data", usecols=lambda x: x not in columns_to_skip, skipfooter=2)

# Filter the rows where "Subject Descriptor" is "Population"
df_unemployment = df_unemployment[df_unemployment["Subject Descriptor"] == "Unemployment rate"]

# Drop the "Subject Descriptor" column
df_unemployment = df_unemployment.drop("Subject Descriptor", axis=1)

# Discard the rightmost 1 columns
df_unemployment = df_unemployment.iloc[:, :-1]  # Exclude the first and last columns

# Load the excel file for per capita military expenditure by country data
xls = pd.ExcelFile(r'D:\Projects\datathon23\datasets\Military_Expenditure_by_ountry.xlsx')

# Define a list of columns to include or exclude
columns_to_skip = ["Notes", "Reporting year"]  # Replace with the actual column names you want to skip

# Read the Excel file and skip specified rows, columns, and the last 8 rows
df_military = pd.read_excel(xls, sheet_name="Share of Govt. spending", skiprows=7, usecols=lambda x: x not in columns_to_skip, skipfooter=7)

# Replace non-numeric values with NaN
df_military = df_military.replace('. .', np.nan)

df_military.iloc[:, 1:] = df_military.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Define a function to create a correlation heatmap with better labels
def create_correlation_heatmap(data1, data2, title, cmap, label1, label2):
    # Join the dataframes on the "Country" column
    merged_data = data1.merge(data2, on="Country", suffixes=("_" + label1, "_" + label2))
    
    # Select only numeric columns for correlation calculation
    numeric_data = merged_data.select_dtypes(include=[np.number])
    
    corr = numeric_data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap)
    plt.title(title)
    plt.xlabel(label1)
    plt.ylabel(label2)
    # Customize x and y axis labels
    ax = plt.gca()
    ax.set_xticklabels([label.get_text().split('_')[0] for label in ax.get_xticklabels()])
    ax.set_yticklabels([label.get_text().split('_')[0] for label in ax.get_yticklabels()])
    plt.show()

# Create a correlation heatmap for Share of government spending on military vs. Inflation
create_correlation_heatmap(df_military, df_inflation, "Correlation Heatmap - Military vs. Inflation", "viridis",
                           "Military Spending Share", "Inflation")

# Create a correlation heatmap for Share of government spending on military vs. Unemployment rate
create_correlation_heatmap(df_military, df_unemployment, "Correlation Heatmap - Military vs. Unemployment", "plasma",
                           "Military Spending Share", "Unemployment Rate")
