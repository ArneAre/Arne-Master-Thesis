# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 00:49:14 2024

@author: arnea
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the DataFrame
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_preprocessedv4.csv')

# Check for 'gas' in 'Article_Text'
df['Contains_Gas'] = df['Article_Text'].str.contains(' gas ', case=False, na=False)
gas_count = df['Contains_Gas'].sum()

# Check for token 'gas' and 'gases' in 'Processed_Article'
df['Token_Gas_Gases'] = df['Article_Text'].str.contains(r'\bgas(es)?\b', case=False, na=False)
token_gas_gases_count = df['Token_Gas_Gases'].sum()

# Check for token 'ga' in 'Processed_Article'
df['Token_Ga'] = df['Processed_Article'].str.contains(r'\bga\b', case=False, na=False)
token_ga_count = df['Token_Ga'].sum()

# Create histograms
plt.figure(figsize=(12, 12))

# Histogram for 'gas' in 'Article_Text'
plt.subplot(4, 1, 1)
df['Contains_Gas'].value_counts().plot(kind='bar', color='skyblue')
plt.title(f'Articles Containing the Word "gas": {gas_count} articles')
plt.xlabel('Contains Gas')
plt.ylabel('Number of Articles')

# Histogram for token 'gas' or 'gases' in 'Processed_Article'
plt.subplot(4, 1, 2)
df['Token_Gas_Gases'].value_counts().plot(kind='bar', color='lightgreen')
plt.title(f'Articles Containing the Token "gas" or "gases": {token_gas_gases_count} articles')
plt.xlabel('Token Gas or Gases')
plt.ylabel('Number of Articles')

# Histogram for token 'ga' in 'Processed_Article'
plt.subplot(4, 1, 3)
df['Token_Ga'].value_counts().plot(kind='bar', color='salmon')
plt.title(f'Articles Containing the Token "ga": {token_ga_count} articles')
plt.xlabel('Token Ga')
plt.ylabel('Number of Articles')

plt.tight_layout()
plt.show()
