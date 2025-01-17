# %%
import re
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from joblib import Parallel, delayed
from scipy.sparse import vstack
from scipy.stats import chi2_contingency
import scipy.stats as stats

# %%
data = pd.read_csv('setp_final_dataset.csv')

# %%
data.shape

# %%
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)     # Show all rows

# %%
def check_null_values(df, column_name):
    total_values = df[column_name].shape[0]  # Total number of rows in the DataFrame
    missing_count = df[column_name].isnull().sum()  # Count of missing values
    missing_percentage = (missing_count / total_values) * 100  # Percentage of missing values
    
    return f"Null count: {int(missing_count)}", f"Null percentage: {float(round(missing_percentage, 2))}%"

# %%
data.head()

# %%
# List of scolumns to train model
featured_columns = ['Product_id', 'Fashion_type', 'Brand_Name', 'category', 'Rating', 'Rating_count_numeric', '5_star', '4_star', '3_star', '2_star', '1_star', 'Occasion', 'Length', 'Wash Care', 'Fit', 'image_ref', 'file_path', 'image_url', 'Fabric', 'Fabric 3', 'Blouse Fabric', 'Fabric 2', 'Fabric Type', 'Lehenga Fabric', 'Lining Fabric', 'Lehenga Lining Fabric', 'Dupatta Fabric']

model_data = data[featured_columns]

# Display the new DataFrame
model_data.head()

# %%
# Check how many missing values are in the 'Fabric' column
missing_fabric_count = model_data['Fabric'].isnull().sum()

# Display the number of missing values in the 'Fabric' column
print(f"Number of missing values in 'Fabric': {missing_fabric_count}")

# Rows where 'Fabric' is missing
missing_fabric_rows = model_data[model_data['Fabric'].isnull()]
missing_fabric_rows.head(10)  # Display the first 10 rows with missing 'Fabric'

# %%
# List of columns to check for missing values in the specified order
fabric_duplicates = model_data[['Fabric 2', 'Fabric 3', 'Fabric Type', 'Blouse Fabric', 'Lehenga Fabric', 'Lining Fabric', 'Lehenga Lining Fabric', 'Dupatta Fabric']]

# Function to impute missing 'Fabric' values
def impute_fabric(row):
    # If 'Fabric' is missing, check other columns in the specified order
    if pd.isnull(row['Fabric']):
        for col in fabric_duplicates:
            if pd.notnull(row[col]):  # If a non-null value is found, use it for 'Fabric'
                return row[col]
    return row['Fabric']  # If 'Fabric' is not missing or no non-null value is found, return the original

# Apply the function to the DataFrame using .loc to avoid SettingWithCopyWarning
model_data.loc[:, 'Fabric'] = model_data.apply(impute_fabric, axis=1)

# Display the updated DataFrame
model_data.head(10)


# %%
# Check how many missing values are in the 'Fabric' column
missing_fabric_count_after= model_data['Fabric'].isnull().sum()

# Display the number of missing values in the 'Fabric' column
print(f"Number of missing values in 'Fabric': {missing_fabric_count_after}")

# Rows where 'Fabric' is missing
missing_fabric_rows = model_data[model_data['Fabric'].isnull()]
missing_fabric_rows.head(10)  # Display the first 10 rows with missing 'Fabric'


# %%
# Display the number of missing values imputed in the 'Fabric' column
print(f"Number of missing values imputed in 'Fabric': {missing_fabric_count-missing_fabric_count_after}")

# %%
# Calculate the percentage of missing values in the 'Fabric' column
null_percentage_fabric = model_data['Fabric'].isnull().mean() * 100

# Display the percentage of missing values
print(f"Percentage of missing values in 'Fabric': {null_percentage_fabric:.2f}%")

# %%
model_data.shape

# %%
# Rearrange columns to move 'Fabric' after 'category'
columns = model_data.columns.tolist()

# Move 'Fabric' to after 'category'
columns.remove('Fabric')
columns.insert(columns.index('category') + 1, 'Fabric')

# Reorder the DataFrame columns
model_data = model_data[columns]
model_data.head()

# %%
# Impute missing values in the 'Fabric' column as 'unknown'
model_data['Fabric'] = model_data['Fabric'].fillna('unknown')

# %%
check_null_values(model_data, 'Fabric')

# %%
# Drop the specified columns from the DataFrame
model_data.drop(columns=fabric_duplicates, inplace=True)

# Display the updated DataFrame to confirm the columns were dropped
model_data.head(10)

# %%


# %%
# Visualize the distribution of Rating
plt.figure(figsize=(10, 5))
sns.histplot(model_data['Rating'], bins=20, kde=True)
plt.title('Distribution of Ratings')
plt.show()


# %% [markdown]
# Quantile Calculation: 
# 
# >Rating Thresholds: Calculate the 33rd percentile and 66th percentile of the Rating column.
# >Count Thresholds: Calculate the 33rd percentile and 66th percentile of the Rating_count_numeric column.
# 
# >High: If the product's rating is above the 66th percentile and its rating count is also above the 66th percentile.
# >Medium: If the product's rating is above the 33rd percentile and its rating count is above the 33rd percentile but below the 66th percentile.
# >Low: Any product that doesn't meet the criteria for high or medium popularity.
# 
# >Using quantiles helps create a fair distribution of popularity categories that reflects the actual data, reducing bias.
# >The thresholds automatically adjust based on the characteristics of the dataset, ensuring that the classification is relevant to the data.

# %%
# Calculate quantiles for Rating and Rating Count
rating_thresholds = model_data['Rating'].quantile([0.33, 0.66]).values
count_thresholds = model_data['Rating_count_numeric'].quantile([0.33, 0.66]).values

# Define a function to categorize popularity based on quantiles
def categorize_popularity(row):
    rating = row['Rating']
    count = row['Rating_count_numeric']

    if rating >= rating_thresholds[1] and count >= count_thresholds[1]:  # High
        return 'high'
    elif rating >= rating_thresholds[0] and count >= count_thresholds[0]:  # Medium
        return 'medium'
    else:  # Low
        return 'low'

# Apply the function to create the 'Popularity' column
model_data['Popularity'] = model_data.apply(categorize_popularity, axis=1)
model_data.head(10)

# %%
Rating_columns= model_data[['Rating', 'Rating_count_numeric', '5_star', '4_star', '3_star', '2_star', '1_star']]

# Drop the specified columns from the DataFrame
model_data.drop(columns=Rating_columns, inplace=True)

# Display the updated DataFrame to confirm the columns were dropped
model_data.head(10)

# %%
# Rearrange columns to move 'Fabric' after 'category'
columns = model_data.columns.tolist()

# Move 'Fabric' to after 'category'
columns.remove('Popularity')
columns.insert(columns.index('Fabric') + 1, 'Popularity')

# Reorder the DataFrame columns
model_data = model_data[columns]
model_data.head()

# %%
check_null_values(model_data, 'image_ref')

# %%
missing_rows = model_data[model_data['image_ref'].isnull()]
display(missing_rows)

# %%
model_data = model_data.dropna(subset=['image_ref'])
model_data.shape

# %%
check_null_values(model_data, 'image_ref')

# %%
check_null_values(model_data, 'Occasion')

# %%
model_data['Occasion'].unique()

# %%
plt.figure(figsize=(12, 6))
sns.countplot(data=model_data, x='Occasion', order=model_data['Occasion'].value_counts().index)
plt.title('Count of Products by Occasion')
plt.xlabel('Occasion')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# %% [markdown]
# Check if Occasion correlates with Fashion_type, category
# 
# >Degrees of Freedom (dof): The number of independent ways the contingency table values can vary.
# 
# >Expected Values (ex_fashion, ex_category): These are the counts we would expect if the variables were independent.

# %%
# Crosstab for Occasion and Fashion_type
occasion_fashion_crosstab = pd.crosstab(model_data['Occasion'], model_data['Fashion_type'])
display(occasion_fashion_crosstab)

# %%
# Crosstab for Occasion and category
occasion_category_crosstab = pd.crosstab(model_data['Occasion'], model_data['category'])
display(occasion_category_crosstab)

# %%
# Heatmap for Occasion and Fashion_type
plt.figure(figsize=(10, 6))
sns.heatmap(occasion_fashion_crosstab, annot=True, fmt="d", cmap="YlGnBu")
plt.title('Occasion vs Fashion_type')
plt.show()

# Heatmap for Occasion and category
plt.figure(figsize=(10, 6))
sns.heatmap(occasion_category_crosstab, annot=True, fmt="d", cmap="YlGnBu")
plt.title('Occasion vs Category')
plt.show()

# %%
# Perform Chi-Square Test for Occasion and Fashion_type
chi2_fashion, p_fashion, dof_fashion, ex_fashion = chi2_contingency(occasion_fashion_crosstab)
print(f"Chi-Square Test between Occasion and Fashion_type: p-value = {p_fashion}")

# Display the results
print(f"Chi-Square Test between Occasion and Fashion_type: p-value = {p_fashion}")

# Interpretation
if p_fashion < 0.05:
    print("There is a significant relationship between Occasion and Fashion_type.")
else:
    print("No significant relationship between Occasion and Fashion_type.")


# %%
# Perform Chi-Square Test for Occasion and category
chi2_category, p_category, dof_category, ex_category = chi2_contingency(occasion_category_crosstab)
print(f"Chi-Square Test between Occasion and category: p-value = {p_category}")


# Display the results
print(f"Chi-Square Test between Occasion and category: p-value = {p_category}")

# Interpretation

if p_category < 0.05:
    print("There is a significant relationship between Occasion and Category.")
else:
    print("No significant relationship between Occasion and Category.")


# %%
occasion_fashion_crosstab.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Bar Plot of Occasion vs Fashion Type')
plt.xlabel('Occasion')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Fashion Type')
plt.show()

# %%

occasion_category_crosstab.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Bar Plot of Occasion vs Category Type')
plt.xlabel('Occasion')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Category Type')
plt.show()

# %% [markdown]
# Since there's a strong relationship between Occasion and Fashion_type or category, impute missing values for Occasion with most common combination of Fashion_type for each occasion.

# %%
def fill_missing_occasion(df):
    def fill_with_mode(group):
        mode_value = group.mode()  # Get the mode of the group
        if not mode_value.empty:
            return group.fillna(mode_value[0])  # Fill missing values with mode
        else:
            return group.fillna('unknown')  # If no mode is found, fill with 'unknown'

    # Fill missing values based on 'Fashion_type'
    df['Occasion'] = df.groupby('Fashion_type')['Occasion'].transform(fill_with_mode)

    # Fill any remaining NaN values based on 'category'
    df['Occasion'] = df.groupby('category')['Occasion'].transform(fill_with_mode)

    return df


# %%
# Apply the combined function
model_data = fill_missing_occasion(model_data)

# %%
check_null_values(model_data, 'Occasion')

# %%
model_data.shape

# %%
model_data.head(10)

# %%
check_null_values(model_data, 'Length')

# %%
model_data['Length'].unique()

# %% [markdown]
# Hence it has 50% missing values, and for the length feature, it's not a ideal to impute a specific value. so we can impute unknown or can drop the feature because it's not that important for the model.

# %%
# Impute missing values in the 'Wash Care' column as 'unknown'
model_data['Length'] = model_data['Length'].fillna('unknown')

# %%
check_null_values(data, 'Wash Care')

# %%
data['Wash Care'].unique()

# %%
# Impute missing values in the 'Wash Care' column as 'unknown'
model_data['Wash Care'] = model_data['Wash Care'].fillna('unknown')

# %%
check_null_values(data, 'Fit')

# %%
data['Fit'].unique()

# %%
# Impute missing values in the Fit column as 'unknown'
model_data['Fit'] = model_data['Fit'].fillna('unknown')

# %%
model_data.head(10)

# %%
print("DataFrame Info:")
model_data.info()

# %%
# Count of unique values in each column
print("\nUnique Values Count:")
print(model_data.nunique())

# %%
# Check for null values and their percentage in each column
null_count = model_data.isnull().sum()  # Count of null values
total_count = model_data.shape[0]  # Total number of rows
null_percentage = (null_count / total_count) * 100  # Percentage of null values

# Create a DataFrame to display the results
null_info = pd.DataFrame({
    'Null Count': null_count,
    'Null Percentage': null_percentage
})

# Display the null information
print(null_info[null_info['Null Count'] > 0])  # Show only columns with null values


# %%
model_data.shape

# %%
model_data.to_csv('processed_dataset.csv', index=False)

# %%



