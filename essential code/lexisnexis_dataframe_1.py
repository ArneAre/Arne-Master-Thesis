# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:10:08 2024

@author: arnea
"""

import pandas as pd
import re
from bs4 import BeautifulSoup

# Specifying the file path
file_path = 'C:/Users/arnea/Desktop/Thesis/india_coal.jsonl/lexis_india_coal.json'

df = pd.read_json(file_path, lines=True)

# Extracting the article text from the "Content" part of the "Document" column which includes the actual article texts 
def extract_article_text(row):
    try:
        # Converting to string, in case the row is not already a string
        row_str = str(row)

        # Extracting the json-like string within the cell
        match = re.search(r"'Content':\s*'(.+?)'}", row_str)
        if match:
            # Extracting the html content within "Content"
            html_content = match.group(1)

            # Parsing the html content with the BeautifulSoup package
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extracting text from the paragraphs within the <bodyText> tags
            body_text = soup.find_all('p')
            return ' '.join(p.get_text(strip=True) for p in body_text)
        else:
            return ''  # Returning empty string if no match found
    except Exception as e:
        print("Error processing row:", e)
        return ''  # Returning empty string in case of error

# Applying the function to the "Document" column
df['Article_Text'] = df['Document'].apply(extract_article_text)

# Displaying the dataframe with the article text
print(df[['Article_Text']].head())

#Extracting the classifications from the "Document" column
def extract_classifications(html_content, classification_scheme):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all 'classification' tags and then filter for the desired scheme in Python
    classifications = soup.find_all('classification')
    class_names = []

    for classification in classifications:
        # Check if the classificationScheme matches the desired scheme
        if classification.get('classificationscheme', '').lower() == classification_scheme:
            class_items = classification.find_all('classificationitem')
            for item in class_items:
                class_name = item.find('classname')
                if class_name and class_name.text:
                    class_names.append(class_name.text)

    return '; '.join(class_names) if class_names else pd.NA

def extract_data_from_document(row, scheme):
    try:
        # Checking if row is a dictionary and has 'Content' key
        if isinstance(row, dict) and 'Content' in row:
            content = row['Content']  # Directly use the 'Content' from the dict
            return extract_classifications(content, scheme)
        else:
            return pd.NA
    except Exception as e:
        print(f"Error processing row: {e}")
        return pd.NA  # Use pd.NA for missing values

# Creating a new column for each classification scheme and populating it
for scheme in ['language', 'city', 'state', 'country']:
    df[scheme.capitalize()] = df['Document'].apply(extract_data_from_document, scheme=scheme.lower())

# Displaying the DataFrame to verify the new columns
print(df.head())


# Saving the dataframe to .csv
df.to_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/dfv1.csv')
