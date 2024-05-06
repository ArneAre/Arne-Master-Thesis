# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:48:31 2024

@author: arnea
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the DataFrame
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_preprocessedv5.csv')

# Check for 'html' in 'Article_Text'
df['Contains_html'] = df['Article_Text'].str.contains(' html ', case=False, na=False)
html_count = df['Contains_html'].sum()

# Check for 'www' in 'Article_Text'
df['Contains_www'] = df['Article_Text'].str.contains(' www ', case=False, na=False)
www_count = df['Contains_www'].sum()

# Check for token 'html' in 'Processed_Article'
df['Token_html'] = df['Processed_Article'].str.contains(r'html', case=False, na=False)
token_html_count = df['Token_html'].sum()

# Create histograms
plt.figure(figsize=(12, 12))

# Histogram for 'html' in 'Article_Text'
plt.subplot(4, 1, 1)
df['Contains_html'].value_counts().plot(kind='bar', color='skyblue')
plt.title(f'Articles Containing the Word "html": {html_count} articles')
plt.xlabel('Contains html')
plt.ylabel('Number of Articles')

# Histogram for 'www' in 'Article_Text'
plt.subplot(4, 1, 2)
df['Contains_www'].value_counts().plot(kind='bar', color='skyblue')
plt.title(f'Articles Containing the Word "www": {www_count} articles')
plt.xlabel('Contains www')
plt.ylabel('Number of Articles')

# Histogram for token 'ga' in 'Processed_Article'
plt.subplot(4, 1, 3)
df['Token_html'].value_counts().plot(kind='bar', color='salmon')
plt.title(f'Articles Containing the Token "ga": {token_html_count} articles')
plt.xlabel('Token Ga')
plt.ylabel('Number of Articles')
