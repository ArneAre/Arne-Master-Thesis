 # -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 22:14:41 2024

@author: arnea
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from wordcloud import WordCloud
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

# Ensuring necessary NLTK downloads
nltk.download('punkt')

# Loading the DataFrame and parsing 'Date' as a datetime object
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_preprocessedv7.csv', parse_dates=['Date'])

# Generating a histogram of articles over time on a monthly basis
df['YearMonth'] = df['Date'].dt.to_period('M')
plt.figure(figsize=(14, 7))  # Increased figure size
ax = df.groupby('YearMonth').size().plot(kind='bar', width=0.8)
plt.title('Number of Articles Over Time (Monthly)')
plt.xlabel('Year and Month')
plt.ylabel('Number of Articles')
# Setting a ticker to control the density of the x-axis labels
tick_spacing = 3
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
plt.xticks(rotation=45, ha='right')  # Adjusting rotation and alignment
plt.grid(axis='x', linestyle='--', color='gray', alpha=0.7)
plt.tight_layout()
plt.show()

# Generating a distribution plot for news outlets
plt.figure(figsize=(12, 8))
sns.countplot(y='Publication', data=df, order=df['Publication'].value_counts().index)
plt.title('Distribution of News Outlets')
plt.xlabel('Count')
plt.ylabel('News Outlet')
plt.show()

#Generating a distribution plot for only the business dailies
df['Date'] = pd.to_datetime(df['Date'])
# List of target publications
publications = ["The Economic Times", "Business Standard", "The Hindu BusinessLine", "The Financial Express", "Mint"]
# Filter the dataframe for the selected publications
filtered_df = df[df['Publication'].isin(publications)]
# Creating the plot
plt.figure(figsize=(14, 7))  # Set the figure size
ax = filtered_df.groupby(['YearMonth', 'Publication']).size().unstack(fill_value=0).plot(kind='bar', stacked=True, width=0.8, ax=plt.gca())
plt.title('Number of Articles by Publication Over Time (Monthly)')
plt.xlabel('Year and Month')
plt.ylabel('Number of Articles')
tick_spacing = 3
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
plt.xticks(rotation=45, ha='right')  # Adjusting the rotation and alignment of x-axis labels
plt.grid(axis='x', linestyle='--', color='gray', alpha=0.7)
plt.tight_layout()
plt.show()

# Generating a histogram for the distribution of article length
plt.figure(figsize=(12, 6))
sns.histplot(df['WordCount'], bins=50, kde=True)
plt.title('Distribution of Article Length')
plt.xlabel('Word Count')
plt.ylabel('Frequency')
plt.show()

# Counting the frequency of the word "coal" in each preprocessed article
df['CoalCount'] = df['Processed_Article'].apply(lambda x: word_tokenize(x).count('coal'))

# Generating a histogram for the frequency of the word "coal"
#plt.figure(figsize=(12, 6))
#sns.histplot(df['CoalCount'], bins=70, kde=True)
#plt.title('Frequency Distribution of the Word "Coal"')
#plt.xlabel('Count of "Coal"')
#plt.ylabel('Number of Articles')
#plt.show()

#Generating a table of the most common tokens
# Tokenizing the preprocessed text to create a list of tokens
tokens = []
for article in df['Processed_Article'].dropna():
    tokens.extend(article.split())
# Counting the frequency of each token
token_counts = Counter(tokens)
# Converting the token counts to a DataFrame
token_counts_df = pd.DataFrame(token_counts.items(), columns=['Token', 'Frequency'])
# Sorting the DataFrame by frequency in descending order
token_counts_df = token_counts_df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)
# Displaying the top N most common tokens
N = 50
top_tokens_df = token_counts_df.head(N)
print(top_tokens_df)


# Generating a word cloud from the preprocessed articles
def tokenize_and_rejoin(text):
    tokens = text.split()  # Split the preprocessed text into tokens
    return ' '.join(tokens)  # Rejoin the tokens into a single string

# Applying the tokenization and rejoining to the preprocessed articles
tokenized_text = df['Processed_Article'].dropna().apply(tokenize_and_rejoin)

# Combining all tokenized texts into one large string
combined_text = ' '.join(tokenized_text)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Preprocessed Articles')
plt.show()