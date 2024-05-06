# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 21:06:00 2024

@author: arnea
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# Importing the dataframe I created
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_cleanedv4.csv')

# Filling NAs in the dataframe with an empty string
df['Article_Text'] = df['Article_Text'].fillna('')

# Function to calculate similarities and include similarity scores
def calculate_similarities(df, threshold=0.80):
    # Vectorizing the text data
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['Article_Text'])
    # Calculating Cosine Similarity
    cos_sim = cosine_similarity(tfidf_matrix)
    
    # Identifying articles with similarity above the threshold
    # and including similarity scores
    duplicates = []
    for i in range(cos_sim.shape[0]):
        for j in range(i + 1, cos_sim.shape[1]):
            if cos_sim[i, j] > threshold:
                Article_Text_1 = df.loc[df.index[i], 'Article_Text']
                Article_Text_2 = df.loc[df.index[j], 'Article_Text']
                duplicates.append((df.index[i], df.index[j], cos_sim[i, j], Article_Text_1, Article_Text_2))
    
    return duplicates

# Applying the function to the entire DataFrame
duplicate_articles = calculate_similarities(df)

# Converting to DataFrame
duplicates_df = pd.DataFrame(duplicate_articles, columns=['Article_Index_1', 'Article_Index_2', 'Similarity_Score', 'Article_Text_1', 'Article_Text_2'])

# Inspecting the duplicates with scores
print(duplicates_df)

# Saving the duplicates dataframe to .csv    
duplicates_df.to_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/dfduplicatesv2.csv')

# Printing the pairs in the console for inspection
for index, row in duplicates_df.iterrows():
    print("Duplicate Pair:")
    print("Article 1:\n", df.loc[row['Article_Index_1'], 'Article_Text'])
    print("Article 2:\n", df.loc[row['Article_Index_2'], 'Article_Text'])
    print("\n")

# Kernel density plot of similarity scores
plt.figure(figsize=(10, 6))
sns.kdeplot(duplicates_df['Similarity_Score'], bw_adjust=0.5)
plt.title('Kernel Density Plot of Similarity Scores')
plt.xlabel('Similarity Score')
plt.ylabel('Density')
plt.grid(True)
plt.show()


# Filtering for similarity scores above my chosen threshold
high_similarity = duplicates_df[duplicates_df['Similarity_Score'] > 0.8]

# Flattening the list of all article indices considered duplicates
duplicate_indices_flat = pd.concat([high_similarity['Article_Index_1'], high_similarity['Article_Index_2']]).unique()

# Marking the first occurrence of each article as not a duplicate
df['is_duplicated'] = df.index.isin(duplicate_indices_flat)
df['duplicate_mark'] = df.duplicated(subset=['Article_Text'], keep='first') | df['is_duplicated']

# Removing marked duplicates
df_nodup = df[~df['duplicate_mark']]

# Dropping the helper columns
df_nodup = df_nodup.drop(columns=['is_duplicated', 'duplicate_mark'])

# Checking the result
print(df_nodup.head())

# Saving the filtered DataFrame
df_nodup.to_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_no_duplicatesv5.csv', index=False)
