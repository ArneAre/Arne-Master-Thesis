# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 13:58:46 2024

@author: arnea
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_preprocessedv2.csv', parse_dates=['Date'])
topics_df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/dtm_topics_over_time.csv')

df['YearMonth'] = df['Date'].dt.to_period('M')
timestamps = df['YearMonth'].dt.strftime('%Y-%m').unique().tolist()
time_slices = [df['YearMonth'].value_counts()[period] for period in sorted(df['YearMonth'].unique())]

# Number of topics
num_topics = 20

# Initialize a DataFrame to store the topic proportions over time
topic_proportions_over_time = pd.DataFrame()

for time_slice in range(len(time_slices)):
    # Initialize a list to store the topic proportions for the current time slice
    topic_proportions = []

    for topic_id in range(num_topics):
        # Extract the topic's proportion for the current time slice and append to the list
        topic_proportions.append(model.show_topic(topicid=topic_id, time=time_slice, topn=0))

    # Convert the list of topic proportions to a DataFrame with one row per topic and one column per time slice
    df_time_slice = pd.DataFrame(topic_proportions).transpose()
    df_time_slice.columns = [f'Topic {i+1}' for i in range(num_topics)]

    # Append the DataFrame for the current time slice to the overall DataFrame
    topic_proportions_over_time = pd.concat([topic_proportions_over_time, df_time_slice], axis=0)

# Set the index of the DataFrame to the time slices (assuming you have a list of time slice labels, e.g., ['Jan 2019', 'Feb 2019', ...])
topic_proportions_over_time.index = [f'Time Slice {i+1}' for i in range(len(time_slices))]

# Plot the topic proportions over time
plt.figure(figsize=(15, 10))
for topic in topic_proportions_over_time.columns:
    plt.plot(topic_proportions_over_time.index, topic_proportions_over_time[topic], label=topic)

plt.title('Topic Prominence Over Time')
plt.xlabel('Time Slice')
plt.ylabel('Average Topic Proportion')
plt.xticks(rotation=45)
plt.legend()
plt.show()
