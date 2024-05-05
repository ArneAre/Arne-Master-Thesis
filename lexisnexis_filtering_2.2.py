# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 17:12:22 2024

@author: arnea
"""

import pandas as pd
import re

def remove_patterns(text):
    # Define complex removals before simple pattern matching
    complex_patterns = {
        "For Updates Check": r'For Updates Check[\s\S]*',
        "To view info graphics, click here": r'To view info graphics, click here[\s\S]*',
        "For more tweets and information": r'For more tweets and information[\s\S]*',
        "<strong>": r'<strong>[\s\S]*?<strong>',
        "Also read|": r'Also read\|[\s\S]*?\)',
        "Also Read:": r'Also Read:[\s\S]*?\)',
        "( The Hindu Business Line:http://www.thehindubusinessline.com/ Delivered by )": '',
        "The views expressed in any and all content distributed by": r'The views expressed in any and all content distributed by[\s\S]*?sole discretion\.',
    }
    
    # Apply complex pattern removals
    for key, pattern in complex_patterns.items():
        text = re.sub(pattern, '', text)

    # Define simpler removal or modification patterns
    simple_patterns = [
        r'\(ANI\)', r'\xa0', r'CLICK HERE FOR THE CHART', r'ALSO READ:', r'READ MORE', 
        r'More to come\.', r'\ufeff', r'Details onp4', r'@thehindu\.co\.in', r'<nl/>', 
        r'\\x91', r'\\x92', r'\\x93', r'\\x94',
        r'--IANS', r'--Indo-Asian News Service', r'--ANS', 
        r'\[http:[^\]]*\]', 
        r'SHARE COMMENTS[\s\S]*', 
        r'Newstex',
        r'@[^ ]*',
        r'http[\s\S]*?(?=\s)',  # Remove http and everything after until the next space
        r'www[\s\S]*?(?=\s)',   # Remove www and everything after until the next space
        r'To view the info graphics, click: http://www\.livemint\.com/r/LiveMint/Period1/2014/06/26/Photos/g-coal-\(web\)\.',
        r'To view infographics, please click:http://www\.livemint\.com/r/LiveMint/Period1/2014/09/25/Photos/Coal_timeline_sep\.',
        r'For the full report, log on to http://www\.',
        r'Full report onwww\.toi\.in', 
        r'Full report onwww\.toi\.in\.',
        r'Arjun Srinivas is withwww\.howindialives\.',
        r'\\',  # Removing stray quotes
    ]

    # Process text by removing or modifying each pattern
    for pattern in simple_patterns:
        text = re.sub(pattern, '', text)

    return text


def remove_newstex_disclaimer(text):
    pattern = re.compile(
        r"The views expressed in any and all content distributed by Newstex[\s\S]*?Newstex and its re-distributors expressly reserve the right to delete stories at its and their sole discretion\.",
        flags=re.IGNORECASE
    )
    text = re.sub(pattern, '', text)
    return text



# Example usage with a sample text containing the disclaimer
sample_text = """
Link to the original story. The views expressed in any and all content distributed by Newstex and its re-distributors (collectively, the "Newstex Authoritative Content") are solely those of the respective author(s) and not necessarily the views of Newstex or its re-distributors. Stories from such authors are provided "AS IS," with no warranties, and confer no rights. The material and information provided in Newstex Authoritative Content are for general information only and should not, in any respect, be relied on as professional advice. Newstex Authoritative Content is not "read and approved" before it is posted. Accordingly, neither Newstex nor its re-distributors make any claims, promises or guarantees about the accuracy, completeness, or adequacy of the information contained therein or linked to from such content, nor do they take responsibility for any aspect of such content. The Newstex Authoritative Content shall be construed as author-based content and commentary. Accordingly, no warranties or other guarantees are offered as to the quality of the opinions, commentary or anything else appearing in such Newstex Authoritative Content. Newstex and its re-distributors expressly reserve the right to delete stories at its and their sole discretion.
"""

# Load my DataFrame
df = pd.read_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_cleanedv2.csv')

# Applying the cleaning function to the 'Article_Text' column
df['Article_Text'] = df['Article_Text'].apply(remove_patterns)
df['Article_Text'] = df['Article_Text'].apply(remove_newstex_disclaimer)

# Saving the cleaned DataFrame
df.to_csv('C:/Users/arnea/OneDrive/Desktop/Thesis/Work/Python/df_cleanedv3.csv', index=False)