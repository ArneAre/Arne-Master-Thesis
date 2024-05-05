# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:03:23 2024

@author: arnea
"""

import pandas as pd

# Load your dataset
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_preprocessedv2.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Filtering the DataFrame for the last three years
# Ensure three_years_ago is timezone-aware
three_years_ago = pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=3)
filtered_df = df[df['Date'] >= three_years_ago]

# Grouping by Year-Month and sampling 3 articles per group
reduced_df = filtered_df.groupby(filtered_df['Date'].dt.to_period('M')).apply(lambda x: x.sample(n=3, replace=True)).reset_index(drop=True)

# Display the reduced DataFrame
print(reduced_df)

# Save the reduced DataFrame to a CSV file if needed
reduced_df.to_csv('reduced_preprocessed.csv', index=False)