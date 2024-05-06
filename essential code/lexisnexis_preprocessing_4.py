# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 23:53:39 2024

@author: arnea
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer
nltk.download('stopwords')
nltk.download('punkt')

# Load my DataFrame
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_no_duplicatesv5.csv')

# Fill NA values in 'Article_Text' and 'Date'
df['Article_Text'] = df['Article_Text'].fillna('')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Remove articles with NA in 'Date' and less than 70 words
df['WordCount'] = df['Article_Text'].apply(lambda x: len(word_tokenize(x)))
df = df.dropna(subset=['Date'])
df = df[df['WordCount'] >= 70]

# Preprocessing steps
stop_words = set(stopwords.words('english'))
additional_stopwords = {"said", "must", "will", "may", "new", "can", "one", "two", "three", "four", "five", "html", "also", "like", "however", "would", "make", "could", "year", "ltd", "due", "rake", "since"}
years = {"2010", "2011", "2012", "2013", "2014","2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"}
days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
months = {"January", "january", "Jan", "February", "february", "Feb", "March", "march", "April", "april", "Apr", "May", "may", "June", "june", "July", "july", "August", "august", "September", "september", "Sep", "October", "october", "Oct", "November", "november", "Nov", "December", "december", "Dec"}
all_stopwords = stop_words.union(additional_stopwords, years, days, months)

def preprocess_text(text):
    # Ensure text is a string
    if not isinstance(text, str):
        return text
    # Remove or replace characters that are not letters or standard whitespace
    text = re.sub(r'[^A-Za-z\s]+', ' ', text)
    # Lowercase
    text = text.lower()
    # Remove punctuation and numbers
    tokenizer = RegexpTokenizer(r'\b[a-z]+\b')  # Only alphabetic strings are included
    tokens = tokenizer.tokenize(text)
    # Remove stopwords
    filtered_tokens = [word for word in tokens if word not in all_stopwords]
    # Remove tokens containing digits
    filtered_tokens = [word for word in filtered_tokens if not any(char.isdigit() for char in word)]
    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    # Join the processed tokens back into a single string
    return ' '.join(stemmed_tokens)

# Applying preprocessing to each article
df['Processed_Article'] = df['Article_Text'].apply(preprocess_text)

# Filter articles to keep only those that contain the word 'coal' (case-insensitive)
df = df[df['Processed_Article'].str.contains('coal', case=False)]

# Removing 'coal' and other words not captured by the stop words
df['Processed_Article'] = df['Processed_Article'].str.replace(r'\b(coal|rs|crore|lakh|per|cent|million|tonn|India|india|indian|ad|go|make|carri|net|receiv|includ|base|annual|past|meet|run|around|use|year|day|today|last|ago|of|come|take|mt|km|time|first|requir|newstex|content|cannot|recent|want|give|set|anoth|along|week|ask|made|well|earlier|given|even|far|say|month|total|without|next|follow|expect|among|present|everi|much|besid|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)\b', '', regex=True)

# Saving the preprocessed DataFrame
df.to_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_preprocessedv7.csv', index=False)
