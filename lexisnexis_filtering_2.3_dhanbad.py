# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 18:55:24 2024

@author: arnea
"""

import pandas as pd
import re

# Load my DataFrame
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_cleanedv3.csv')  # Update the path to your CSV file

# Function to filter out specific "coal" phrases in a case-insensitive manner
def filter_coal_contexts(text):
    # Check if "coal" appears outside of the specified contexts
    coal_pattern = re.compile(r'\bcoal\b', re.IGNORECASE)
    # Find all matches
    all_coals = coal_pattern.findall(text)
    # Check if these matches are only as part of the excluded phrases
    specific_coal_pattern = re.compile(r'\bcoal (town|capital|belt)\b', re.IGNORECASE)
    matches = specific_coal_pattern.findall(text)
    # Return True to keep the article if there are other uses of "coal" or if "coal" isn't mentioned
    return len(all_coals) != len(matches)

# Apply the filter function to the DataFrame
df_filtered = df[df['Article_Text'].apply(filter_coal_contexts)]

# Save the filtered DataFrame
df_filtered.to_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_cleanedv4.csv', index=False)  # Update the path to where you want to save the filtered data