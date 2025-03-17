"""
This module performs the text cleaning in the following way:
    -   Remove special characters.
    -   Apply join_letters funtion: after removing the special characters, this function helps to join the single letters.
    -   Remove the commercial words and legal suffixes.
    -   Remove stopwords.
    -   Remove accents.
"""
import re
import unicodedata
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
import os

# Ensure stopwords are downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# print('\nStopwords are downloaded \n')

# # Load the stopwords for 7 languages
# stopwords_es = set(stopwords.words('spanish'))
# stopwords_en = set(stopwords.words('english'))
# stopwords_fr = set(stopwords.words('french'))
# stopwords_de = set(stopwords.words('german'))
# stopwords_it = set(stopwords.words('italian'))
# stopwords_pt = set(stopwords.words('portuguese'))
# stopwords_ru = set(stopwords.words('russian'))

    

# ---------------------------------------  JOIN LETTERS FUNCTION ------------------------------------------------------
def join_letters(text):
    # REMOVE SPACES BETWEEN SINGLE LETTERS AND JOIN THEM TO FORM WORDS
    text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b', r'\1\2\3\4\5\6\7\8', text)  # FOR 8 LETTERS
    text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b', r'\1\2\3\4\5\6\7', text)                 # FOR 7 LETTERS
    text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b', r'\1\2\3\4\5\6', text)                                # FOR 6 LETTERS
    text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b', r'\1\2\3\4\5', text)                                               # FOR 5 LETTERS
    text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b', r'\1\2\3\4', text)                                                              # FOR 4 LETTERS
    text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])\b', r'\1\2\3', text)                                                                             # FOR 3 LETTERS
    text = re.sub(r'\b([a-zA-Z])\s+([a-zA-Z])\b', r'\1\2', text)                                                                                            # FOR 2 LETTERS

    # REPEAT FOR ANY HIGHER COUNT, OR USE A SIMPLE PATTERN TO MATCH ANY SPACE-SEPARATED CAPITAL LETTERS
    text = re.sub(r'\b([A-Z])\s+([A-Z])\s+([A-Z])\b', r'\1\2\3', text) 
    
    return text

# ----------------------------------------- REMOVE COMMERCIAL WORDS AND LEGAL SUFFIXES --------------------------------
# FUNCTION TO LOAD THE DICTIONARIES FOR EACH COUNTRY
def load_banned_words(country_code):
    """
    Load banned word dictionaries based on the country code.
    Dictionaries come from Banned_word_dictionary.

    Args:
        - country_code: The country code.

    Returns:
        - List of banned words (legal suffixes and commercial words).
    """
    banned_words = set()
    file_path = os.path.join("Banned_word_dictionary", f"{country_code}.json")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            banned_words.update(data.get("remove", []))
    
    else:
        print(f'Warning: Dictionary for {country_code} not found.')
    
    return banned_words



def remove_banned_words(text, country_code):
    """
    Remove banned words (legal suffixes and commercial words) from the text based on the country-specific dictionary.
    
    Args:
        - text: The text to be cleaned
        - country_code: The country code to load the appropiate banned words.
    
    Returns:
        - The cleaned text with banned words removed.
    """
    banned_words = load_banned_words(country_code)

    words = text.split()
    cleaned_words = [word for word in words if word not in banned_words]

    return ' '.join(cleaned_words)


# --------------------------------------- REMOVE STOPWORDS ----------------------------------------------------------
# def remove_stopwords(text):
#     """
#     This function removes stop words in the following languages: english, spanish, german and french, italian, portuguese and russian.

#     all_stopwords: Determine the language of the text (you can use a language detection library if needed). 
#     For simplicity, we assume that the language of the sentence is determined by the words in the text.
#     """

#     # Tokenyze the text
#     words = word_tokenize(text)
    
#     all_stopwords = (stopwords_es | stopwords_en | stopwords_fr | 
#                      stopwords_de | stopwords_it | stopwords_pt | stopwords_ru) 

#     cleaned_text = [word for word in words if word not in all_stopwords]
   
#     return ' '.join(cleaned_text)


# --------------------------------------- REMOVE ACCENTS -----------------------------------------------------------
def remove_accents(text):
    """
    Removes accents from a given text.
    """
    # NORMALICE THE TEXT AND REMOVE THE DIACRITICAL MARKS (ACCENTS, TILDES, ETC.)
    normalized_text = ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn'))
    
    # REPLACE "ß" BY "ss"  
    normalized_text = normalized_text.replace("ß", "ss")
    
    return normalized_text


## -------------------------------------- CLEAN TEXT FUNCTION -------------------------------------------------------
# COMPILE ALL THE FUNCTION TO CLEAN TEXT 

def clean_text(text: str, country_code: str):
    """
    Applues all the text cleaning functions in the correct order:
    1. Removes special characters
    2. Removes common phrases
    3. Merges and removes legal suffixes
    4. Removes stopwords
    5. Removes accents  
    """
    if not isinstance(text, str) or pd.isna(text):
        return ""
    
    # REMOVE SPECIAL CHARACTERS 
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()

    text = join_letters(text)
    text = remove_banned_words(text, country_code)
    text = remove_accents(text)

    return text