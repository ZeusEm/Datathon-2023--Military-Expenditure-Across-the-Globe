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

"""
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

# Group smaller countries into an "Others" category
country_sales = df_2021.groupby('Country')['Arms Sales (2021)'].sum()
top_countries = country_sales.nlargest(12)
other_countries = country_sales[~country_sales.index.isin(top_countries.index)].sum()
top_countries['Others'] = other_countries

# Get the top 5 companies in the legend
top_5_companies = df_2021.groupby('Country')['Company'].sum().value_counts()[:5].index

# Create a custom colormap for the stacked bar chart
custom_colormap = plt.cm.get_cmap('tab20', len(top_countries.index))

# Increase the overall plot size
fig, ax = plt.subplots(figsize=(16, 8))

# Create a stacked bar chart for the year 2021 with the top 10 countries and an "Others" category
top_countries.plot(kind='bar', stacked=True, colormap=custom_colormap, ax=ax, width=0.9)  # Adjust width for spacing
ax.set_xlabel('Country')
ax.set_ylabel('Arms Sales (in millions of US$)')
ax.set_xticks(range(len(top_countries.index)))
# Replace the last label with "Others"
xtick_labels = list(top_countries.index)
xtick_labels[-1] = 'Others'
ax.set_xticklabels(xtick_labels, rotation=45)  # Rotate x-axis labels
ax.legend(title='Company', labels=top_5_companies)

# Create a line graph depicting global trends in military expenditure
global_trends = df_2021.groupby('Country')['Arms Sales (2021)'].sum().sort_values(ascending=False)[:12]
global_trends.plot(marker='o', linestyle='-', color='b')
ax.set_title('Arms Sales by Country and Global Trends in Military Expenditure - 2021 (Top 10 Countries + Others)')

# Show the "Others" label on the x-axis
ax.set_xticklabels(xtick_labels, rotation=45)
plt.show()
"""





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

for company, color in zip(grouped_data.columns, colors(range(len(grouped_data.columns)))):
    plt.bar(grouped_data.index, grouped_data[company], bottom=bottom, label=company, color=color)
    bottom += grouped_data[company]

# Add a legend for the top 10 companies
plt.legend(title='Company', labels=top_10_companies)

plt.xlabel('Country')
plt.ylabel('Arms Sales (in millions of US$)')
plt.xticks(rotation=45)
plt.title('Arms Sales by Companies and Countries - 2021')
plt.show()
