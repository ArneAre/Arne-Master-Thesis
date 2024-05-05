# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 16:00:54 2024

@author: arnea
"""

import pandas as pd
import re

# Importing the dataframe I created
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/dfv1.csv')

# Removing the word count and the last comma from the 'Overview' column
df['Overview'] = df['Overview'].str.replace(r',\s*\d+words$', '', regex=True)


# Empty Columns to be removed
columns_to_remove = [
    "Location", "WebNewsUrl", "Geography", "NegativeNews", "Industry", "People", "Subject", 
    "Company", "PublicationType", "Publisher", "GroupDuplicates", "SimilarDocuments", 
    "InternationalLocation", "LEI", "CompanyName", "LNGI", "SearchWithinResults", 
    "Exclusions", "ResultId", "SearchType", "Source", "Topic", "PracticeArea", "Keyword", 
    "PostFilters", "AppliedPostFilter", "DocumentContent_odata_mediaContentType", 
    "IsCitationMatch", "SourcePath"
]

# Removing the specified columns, using 'errors='ignore'' to skip any columns that don't exist in the DataFrame
df = df.drop(columns=columns_to_remove, axis=1, errors='ignore')

# Renaming 'Overview' column to 'Publication'
df.rename(columns={'Overview': 'Publication'}, inplace=True)

# Creating a new table with publication counts, average word counts, and median word counts
publication_stats = df.groupby('Publication').agg(
    Article_Count=('Publication', 'size'),
    Average_Word_Count=('WordLength', 'mean'),
    Median_Word_Count=('WordLength', 'median')
).reset_index()

# Displaying the new table
print(publication_stats)


# List of unique newspapers, excluding "The" where applicable
newspapers = [
    "Times Of India", "Hindustan Times", "The Hindu", "Mumbai Mirror", 
    "The Telegraph", "Economic Times", "Mid Day", "Deccan Herald", 
    "Tribune", "Deccan Chronicle", "Indian Express", "New Indian Express",
    "Mint", "Business Standard", "Business Line", "Deccan"
]

# Initializing a list to store counts for each newspaper
newspaper_counts = []

# Looping through each newspaper and counting its occurrences in the dataset
for newspaper in newspapers:
    # Using str.contains to find occurrences of each newspaper name, excluding "The" from the search to account for it left out for some publications
    # The `na=False` parameter ensures NaN values are treated as False in the search
    count = df['Publication'].str.contains(newspaper, case=False, na=False).sum()
    newspaper_counts.append((newspaper, count))

# Creating a DataFrame from the counts
newspaper_counts_df = pd.DataFrame(newspaper_counts, columns=['Newspaper', 'Article Count'])

# Displaying the DataFrame
print(newspaper_counts_df)


# List of publication keywords to filter
publication_keywords = [
    "Hindustan Times", 
    "Telegraph",
    "Business Line", 
    "Financial Express", 
    "Times of India", "TOI", 
    "Economic Times", 
    "Indian Express", 
    "The Hindu", "Hindu", 
    "Business Standard",
    "Deccan Herald",
    "Mint",
    "Tribune",
    "Pioneer",
    "United News of India", "UNI",
    "Asian News International", "ANI",
    "Indo-Asian News Service", "IANS"
]

filtered_publication_stats = {}

for keyword in publication_keywords:
    # Creating a filtered table for publications that contain the keyword
    filtered_publication_stats[keyword] = publication_stats[publication_stats['Publication'].str.contains(keyword, case=False, na=False)]

#Checking each table
ht_df = filtered_publication_stats["Hindustan Times"]
tele_df = filtered_publication_stats["Telegraph"]
bl_df = filtered_publication_stats["Business Line"]
fe_df = filtered_publication_stats["Financial Express"]
et_df = filtered_publication_stats["Economic Times"]
ie_df = filtered_publication_stats["Indian Express"]
th_df = filtered_publication_stats["The Hindu"]
hindu_df = filtered_publication_stats["Hindu"]
bs_df = filtered_publication_stats["Business Standard"]
toi_df = publication_stats[publication_stats['Publication'].str.contains('Times of India|TOI', case=False, na=False)]
dec_df = filtered_publication_stats["Deccan Herald"]
mint_df = filtered_publication_stats["Mint"]
tri_df = filtered_publication_stats["Tribune"]
pio_df = filtered_publication_stats["Pioneer"]
uni_df = publication_stats[publication_stats['Publication'].str.contains('United News of India|UNI', case=False, na=False)]
ani_df = publication_stats[publication_stats['Publication'].str.contains('Asian News International|ANI', case=False, na=False)]
ians_df = publication_stats[publication_stats['Publication'].str.contains('Indo-Asian News Service|IANS', case=False, na=False)]

print(ht_df.head())

# Unifying the publication name for articles from the same newspaper

# Starting with Hindustan Times
# Function to process the 'Publication' column and extract additional info
def unify_hindustan_times(row):
    if row['Publication'].startswith('Hindustan Times'):
        # Extract additional info if present
        add_info = row['Publication'][len('Hindustan Times'):].strip()
        row['Add Info Publication'] = add_info if add_info else None  # Store additional info if not empty
        row['Publication'] = 'Hindustan Times'  # Unify publication name
    return row

# Ensuring the 'Publication' column is a string
df['Publication'] = df['Publication'].astype(str)

# Applying the function to each row of the DataFrame
df = df.apply(unify_hindustan_times, axis=1)


# The Telegraph
# Replacing "The Telegraph (India)" with "The Telegraph" in the 'Publication' column
df['Publication'] = df['Publication'].replace('The Telegraph (India)', 'The Telegraph')


# Business Line
def unify_business_line(row):
    if 'Business Line' in row['Publication'] or 'The Hindu Business Line' in row['Publication']:
        # Extracting additional info if present (e.g., page numbers)
        add_info = row['Publication'].replace('Business Line', '').replace('The Hindu Business Line', '').strip(', ')
        row['Add Info Publication'] = add_info if add_info else None  # Storing additional info if not empty
        row['Publication'] = 'The Hindu BusinessLine'  # Unifying the publication name
    return row

df = df.apply(unify_business_line, axis=1)


# The Financial Express
# Function to unify publication names to "The Financial Express", excluding those with "Bangladesh"
def unify_financial_express(publication):
    if 'Financial Express' in publication and 'Bangladesh' not in publication:
        return 'The Financial Express'
    return publication

# Applying the function to the 'Publication' column
df['Publication'] = df['Publication'].apply(unify_financial_express)


# Economic Times
def unify_economic_times(row):
    if 'Economic Times' in row['Publication']:
        # Checking if the publication name contains "(India)" and extract additional info accordingly
        if '(India)' not in row['Publication']:
            # Extract additional info if present
            add_info = row['Publication'].replace('Economic Times (E-Paper Edition)', '').replace('The Economic Times', '').strip(', ')
            row['Add Info Publication'] = add_info if add_info else None  # Store additional info if not empty
        else:
            # For publications containing "(India)", do not extract additional info
            row['Add Info Publication'] = None

        row['Publication'] = 'The Economic Times'  # Unifying publication name

    return row

df = df.apply(unify_economic_times, axis=1)


# The Indian Express & The New Indian Express
def unify_indian_express(row):
    if 'Indian Express' in row['Publication']:
        if row['Publication'].startswith('Indian Express'):
            row['Publication'] = 'The Indian Express' # Updating to "The Indian Express"
            row['Add Info Publication'] = None  # No additional info to extract
        else:
            # For "New Indian Express" and variations with "Bangalore"
            if 'Bangalore' in row['Publication']:
                row['Add Info Publication'] = 'Bangalore'
            else:
                row['Add Info Publication'] = None  # No additional info to extract

            row['Publication'] = 'The New Indian Express'  # Updating to "The New Indian Express"

    return row

df = df.apply(unify_indian_express, axis=1)


# The Hindu
def unify_the_hindu(row):
    # Checking if publication name contains 'The Hindu'
    if 'The Hindu' in row['Publication']:
        # Leaving 'The Hindu BusinessLine' entries untouched
        if 'BusinessLine' not in row['Publication']:
            # Extracting 'Bangalore' to 'Add Info Publication' if present
            if 'Bangalore' in row['Publication']:
                row['Add Info Publication'] = 'Bangalore'
            else:
                row['Add Info Publication'] = None  # No additional info to extract
            
            # Updating publication name to 'The Hindu'
            row['Publication'] = 'The Hindu'

    return row

df = df.apply(unify_the_hindu, axis=1)


# Business Standard
def unify_business_standard(row):
    # Checking if publication name contains 'Business Standard'
    if 'Business Standard' in row['Publication']:
        # Extracting 'Online' to 'Add Info Publication' if present
        if 'Online' in row['Publication']:
            row['Add Info Publication'] = 'Online'
        else:
            row['Add Info Publication'] = None  # No additional info to extract
        
        # Updating publication name to 'Business Standard'
        row['Publication'] = 'Business Standard'

    return row

df = df.apply(unify_business_standard, axis=1)


# The Times of India
def unify_times_of_india(row):
    publication = row['Publication']
    
    # Checking for "TOI" or "Times of India" in the publication name
    if 'TOI' in publication or 'Times of India' in publication:
        # Extracting "TOI.com & ET.com Blogs" if "ET.com" is present
        if 'ET.com' in publication:
            row['Add Info Publication'] = 'TOI.com & ET.com Blogs'
        # Extracting "Bangalore" if "Pg." and "Bangalore" are present
        elif 'Pg.' in publication and 'Bangalore' in publication:
            row['Add Info Publication'] = 'Bangalore'
        # For other cases, extracting everything after "The Times of India"
        else:
            add_info = publication.split('The Times of India', 1)[-1].strip(', ')
            # If "The Times of India" is not in the publication name, consider the entire string after "TOI"
            if add_info == publication:
                add_info = publication.split('TOI', 1)[-1].strip(', ')
            row['Add Info Publication'] = add_info if add_info else None

        # Updating the publication name to "The Times of India"
        row['Publication'] = 'The Times of India'

    return row

df = df.apply(unify_times_of_india, axis=1)


# Deccan Herald
df.loc[df['Publication'].str.contains('Deccan Herald', na=False), 'Publication'] = 'Deccan Herald'


# Mint
def unify_mint_publications(row):
    publication = row['Publication']
    
    # Checking if the publication name contains 'Mint' but not 'MintAsia'
    if 'MINT' in publication or 'Mint' in publication and 'MintAsia' not in publication:
        # For publications containing 'Bangalore', extract it to 'Add Info Publication'
        if 'Bangalore' in publication:
            row['Add Info Publication'] = 'Bangalore'
        else:
            row['Add Info Publication'] = None  # No additional info for others
        
        # Updating publication name to 'Mint'
        row['Publication'] = 'Mint'

    return row

df = df.apply(unify_mint_publications, axis=1)


# The Pioneer
df.loc[df['Publication'].str.contains('The Pioneer', na=False), 'Publication'] = 'The Pioneer'


#IANS
def unify_ians_publications(row):
    # Checking if the publication is "IANS-English" or "Indo-Asian News Service"
    if row['Publication'] in ['IANS-English', 'Indo-Asian News Service']:
        # Updating the publication name to "IANS (Indo-Asian News Service)"
        row['Publication'] = 'IANS (Indo-Asian News Service)'

    return row

# Applying the function to each row of the DataFrame
df = df.apply(unify_ians_publications, axis=1)


#Counting the number of unique publications in the dataset
unique_publications_count = df['Publication'].nunique()
print(unique_publications_count)


# Removing the other publications
# List of specified publication names to keep
specified_publications = [
    'Hindustan Times',
    'The Telegraph',
    'The Hindu BusinessLine',
    'The Financial Express',
    'The Economic Times',
    'The Indian Express',
    'The New Indian Express',
    'The Hindu',
    'Business Standard',
    'The Times of India',
    'Mint',
    'UNI (United News of India)',
    'Asian News International (ANI)',
    'IANS (Indo-Asian News Service)',
]

# Filtering the DataFrame to keep only rows with specified publication names
df_filtered = df[df['Publication'].isin(specified_publications)]

# Displaying the filtered DataFrame to verify the changes
print(df_filtered.head())


#Cleaning up the article texts before duplicate analysis
def cleaning_article(text):
    # Ensuring text is a string
    if not isinstance(text, str):
        return text  # Return the original value if it's not a string
    
    # Removing the starting portion before and including '--' or ':' if within the first 6 words
    text = re.sub(r'^(?:\S+\s+){0,5}(\S*(--|:))', '', text, count=1, flags=re.DOTALL)
    
    # Removing only the sentence containing a web or email address at the end of the article
    text = re.sub(r'[^.!?]*\b(www\.\S+|\S+\.(com|net|org|info|edu))[^.!?]*$', '', text, flags=re.DOTALL)
    
    # Removing everything after "disclaimer:", including "disclaimer:" itself
    text = re.sub(r'\s*disclaimer:.*$', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    return text

# Converting the entire 'Article_Text' column to strings to avoid TypeError
df_filtered['Article_Text'] = df_filtered['Article_Text'].astype(str)

# Applying the preprocessing function to the 'Article_Text' column
df_filtered['Article_Text'] = df_filtered['Article_Text'].apply(cleaning_article)

#Another cleaning step
def cleaning_article2(text):
    # Ensuring text is a string
    if not isinstance(text, str):
        return text  # Return the original value if it's not a string
    
    # Criteria 1: Handling "http://blogs.hindustantimes.com/" in the first 100 characters
    if "http://blogs.hindustantimes.com/" in text[:100]:
        text = re.sub(r'^.*?--', '', text, count=1, flags=re.DOTALL)
        text = re.sub(r'\s*[^.!?]*\.$', '', text, flags=re.DOTALL)  # Removing the last sentence

    # Criteria 3: Removing ".jpg)" within the first 100 characters
    if ".jpg)" in text[:100]:
        text = re.sub(r'^.*?\.jpg\)', '', text, count=1, flags=re.DOTALL)
    
    # Criteria 4: Handling "http://www.thehindubusinessline.com" within the first 100 characters
    if "http://www.thehindubusinessline.com" in text[:100]:
        text = re.sub(r'^.*?\)', '', text, count=1, flags=re.DOTALL)
        text = re.sub(r'\s*[^.!?]*\.$', '', text, flags=re.DOTALL)  # Removing the last sentence
    
    # Criteria 5: Removing text up to "ANI" within the first 80 characters
    if "ANI" in text[:80]:
        text = re.sub(r'^.*?ANI', '', text, count=1, flags=re.DOTALL)

    # Removing the last sentence if it inlcudes "Published by" and "with permission from"
    text = re.sub(r'(?<=\.|\?|!)(\s*[^.!?]*Published by[^.!?]*with permission from[^.!?]*[.!?])$', '', text, flags=re.DOTALL)

    return text

# Applying the preprocessing function to the 'Article_Text' column
df_filtered['Article_Text'] = df_filtered['Article_Text'].apply(cleaning_article2)


#One more cleaning step
def cleaning_article3(row):
    # Extract the article text
    text = row['Article_Text']

    # Criteria 2: Extracting text before the first comma for "(IANS" within the first 50 characters
    if "(IANS" in text[:50]:
        add_info_match = re.match(r'^(.*?),', text)
        if add_info_match:
            # Extract and add the info before the first comma to the "Add Info Publication" column
            row['Add Info Publication'] = add_info_match.group(1)
        # Remove everything up to and including the first ")" after "(IANS"
        text = re.sub(r'^.*?\)', '', text, count=1, flags=re.DOTALL)

    # Apply other criteria as needed, modifying 'text' as required

    # Update the 'Article_Text' column with the cleaned text
    row['Article_Text'] = text
    
    return row

# Applying the cleaning function to each row
df_filtered = df_filtered.apply(cleaning_article3, axis=1)


# Grouping by 'Publication' and aggregate
publication_stats = df_filtered.groupby('Publication').agg(
    Occurrences=('Publication', 'size'),
    Mean_Word_Length=('WordLength', 'mean'),
    Median_Word_Length=('WordLength', 'median')
).reset_index()

# Displaying the aggregated DataFrame to verify the results
print(publication_stats)

# Saving the dataframe to .csv
df_filtered.to_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_cleanedv2.csv')