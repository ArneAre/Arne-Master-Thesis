# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 11:14:51 2024

@author: arnea
"""

import pandas as pd
import ast  # To safely evaluate strings containing Python literals

# Load the data
df = pd.read_csv("C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/dtm_topics_over_timev4.csv")

# The columns are swapped; let's correct that:
df['Temp'] = df['Words']
df['Words'] = df['Weights']
df['Weights'] = df['Temp']
df.drop(columns='Temp', inplace=True)

# Convert the 'Words' and 'Weights' from string representations of lists to actual lists
df['Words'] = df['Words'].apply(ast.literal_eval)
df['Weights'] = df['Weights'].apply(lambda x: [float(weight) for weight in ast.literal_eval(x)])

# Initialize a DataFrame to store the top words for each topic
top_words_df = pd.DataFrame()

# Process each topic
for topic_num in df['TopicNum'].unique():
    topic_data = df[df['TopicNum'] == topic_num]

    # Flatten the lists of words and weights across all time slices
    words = [word for sublist in topic_data['Words'] for word in sublist]
    weights = [weight for sublist in topic_data['Weights'] for weight in sublist]

    # Create a DataFrame from the flattened lists
    topic_words_df = pd.DataFrame({'Word': words, 'Weight': weights})

    # Group by 'Word' and calculate the mean weight
    averaged_weights = topic_words_df.groupby('Word')['Weight'].mean().reset_index()

    # Sort by 'Weight' to find the top 20 words
    top_words = averaged_weights.nlargest(20, 'Weight')

    # Add the topic number for identification
    top_words['TopicNum'] = topic_num

    # Append to the main DataFrame
    top_words_df = pd.concat([top_words_df, top_words], ignore_index=True)


# Optionally, save the result to a new CSV
top_words_df.to_csv('top_words_per_topicv4.csv', index=False)

# Print the DataFrame to verify
print(top_words_df)