# Import necessary packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# # Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the directory where files will be saved
directory = 'C:/Users/Nidhi Dhameliya/Desktop/jupyter/Data_Extraction_and_Text_Analysis_for_Blackcoffer_company/TitleText/'

# Check if the directory exists, if not create it
if not os.path.exists(directory):
    os.makedirs(directory)

# Read the URL file into the pandas object
df = pd.read_excel('Input.xlsx')

# Loop through each row in the df
for index, row in df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']

    # Make a request to the URL with timeout
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=header, timeout=10)
        if response.status_code != 200:
            print(f"Failed to retrieve {url_id} - Status code: {response.status_code}")
            continue
    except requests.exceptions.RequestException as e:
        print(f"Can't get response for {url_id}: {e}")
        continue

    # Create a BeautifulSoup object
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Can't parse page for {url_id}: {e}")
        continue

    # Find title
    try:
        title = soup.find('h1').get_text()
    except Exception as e:
        print(f"Can't get title for {url_id}: {e}")
        title = "No title found"

    # Find text
    article = ""
    try:
        for p in soup.find_all('p'):
            article += p.get_text()
    except Exception as e:
        print(f"Can't get text for {url_id}: {e}")

    # Define file name and write title and text to the file with UTF-8 encoding
    file_name = os.path.join(directory, f"{url_id}.txt")
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(title + '\n' + article)

    print(f"Successfully saved {url_id} content.")


import os
import nltk
from nltk.tokenize import word_tokenize

# Download punkt tokenizer if not already downloaded
nltk.download('punkt')

# Directories
text_dir = "C:/Users/Nidhi Dhameliya/Desktop/jupyter/Data_Extraction_and_Text_Analysis_for_Blackcoffer_company/TitleText"
stopwords_dir = "C:/Users/Nidhi Dhameliya/Desktop/jupyter/Data_Extraction_and_Text_Analysis_for_Blackcoffer_company/StopWords"
sentment_dir = "C:/Users/Nidhi Dhameliya/Desktop/jupyter/Data_Extraction_and_Text_Analysis_for_Blackcoffer_company/MasterDictionary"

# Function to load words from files into a set
def load_words_from_files(directory, encoding='ISO-8859-1'):
    words_set = set()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), 'r', encoding=encoding) as f:
            words_set.update(f.read().splitlines())
    return words_set

# Load stopwords
stop_words = load_words_from_files(stopwords_dir)

# Load positive and negative word lists individually
def load_words_from_file(file_path, encoding='ISO-8859-1'):
    with open(file_path, 'r', encoding=encoding) as f:
        return set(f.read().splitlines())

# Paths to positive and negative word files
positive_file = os.path.join(sentment_dir, 'positive-words.txt')
negative_file = os.path.join(sentment_dir, 'negative-words.txt')

# Load positive and negative words if files exist
if os.path.exists(positive_file):
    pos_words = load_words_from_file(positive_file)
else:
    print(f"Positive words file not found at: {positive_file}")
    pos_words = set()

if os.path.exists(negative_file):
    neg_words = load_words_from_file(negative_file)
else:
    print(f"Negative words file not found at: {negative_file}")
    neg_words = set()

# Remove any overlap between positive and negative words
unique_pos_words = pos_words - neg_words
unique_neg_words = neg_words - pos_words

# Load and process text files
docs = []
for text_file in os.listdir(text_dir):
    with open(os.path.join(text_dir, text_file), 'r', encoding='utf-8') as f:
        text = f.read()
        # Tokenize the given text file and remove stopwords
        words = word_tokenize(text)
        filtered_text = [word.lower() for word in words if word.lower() not in stop_words and word.isalpha()]
        docs.append(filtered_text)

# Sentiment analysis: Calculate scores
positive_words, negative_words = [], []
positive_score, negative_score = [], []
polarity_score, subjectivity_score = [], []

# Iterate through the list of docs
for doc in docs:
    # Find words in the document that match the positive and negative sets
    positive_words_in_doc = [word for word in doc if word in unique_pos_words]
    negative_words_in_doc = [word for word in doc if word in unique_neg_words]

    # Store found words for future reference
    positive_words.append(positive_words_in_doc)
    negative_words.append(negative_words_in_doc)

    # Calculate scores
    pos_score = len(positive_words_in_doc)
    neg_score = len(negative_words_in_doc)

    # Adjust scores to ensure they are not the same unless both are zero
    if pos_score == neg_score and pos_score > 0:
        neg_score += 1  # Slight adjustment to avoid identical scores

    # Append the scores to the lists
    positive_score.append(pos_score)
    negative_score.append(neg_score)

    # Calculate Polarity Score: (Positive Score – Negative Score) / ((Positive Score + Negative Score) + 0.000001)
    polarity = (pos_score - neg_score) / (pos_score + neg_score + 0.000001)
    polarity_score.append(polarity)

    # Calculate Subjectivity Score: (Positive Score + Negative Score) / ((Total Words after cleaning) + 0.000001)
    subjectivity = (pos_score + neg_score) / (len(doc) + 0.000001)  # Avoid division by zero
    subjectivity_score.append(subjectivity)

# Optionally, print or save the scores if needed
for i, doc in enumerate(docs):
    print(f"Document {i+1}:")
    print(f"  Positive Words: {positive_words[i]}")
    print(f"  Negative Words: {negative_words[i]}")
    print(f"  Positive Score: {positive_score[i]}")
    print(f"  Negative Score: {negative_score[i]}")
    print(f"  Polarity Score: {polarity_score[i]}")
    print(f"  Subjectivity Score: {subjectivity_score[i]}")
    print()


import os
import re
from nltk.corpus import stopwords
import nltk
nltk.download('punkt_tab')

# Directories
text_dir = "C:/Users/Nidhi Dhameliya/Desktop/jupyter/Data_Extraction_and_Text_Analysis_for_Blackcoffer_company/TitleText"

stopwords = set(stopwords.words('english'))

def measure(file):
    try:
        # Try opening the file with utf-8 encoding
        with open(os.path.join(text_dir, file), 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Remove punctuations
        text = re.sub(r'[^\w\s.]', '', text)
        
        # Split the text into sentences
        sentences = text.split('.')
        num_sentences = len(sentences)
        
        # Get total words in the file, excluding stopwords
        words = [word for word in text.split() if word.lower() not in stopwords]
        num_words = len(words)
        
        # Identify complex words (words with more than 2 syllables)
        complex_words = []
        for word in words:
            vowels = 'aeiou'
            syllable_count_word = sum(1 for letter in word if letter.lower() in vowels)
            if syllable_count_word > 2:
                complex_words.append(word)
        
        # Syllable count per word
        syllable_count = 0
        syllable_words = []
        for word in words:
            if word.endswith('es'):
                word = word[:-2]
            elif word.endswith('ed'):
                word = word[:-2]
            syllable_count_word = sum(1 for letter in word if letter.lower() in vowels)
            if syllable_count_word >= 1:
                syllable_words.append(word)
                syllable_count += syllable_count_word
        
        # Calculating metrics
        avg_sentence_len = num_words / num_sentences if num_sentences > 0 else 0
        avg_syllable_word_count = syllable_count / len(syllable_words) if syllable_words else 0
        percent_complex_words = len(complex_words) / num_words if num_words > 0 else 0
        fog_index = 0.4 * (avg_sentence_len + percent_complex_words)
        
        return avg_sentence_len, percent_complex_words, fog_index, len(complex_words), avg_syllable_word_count
    
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return 0, 0, 0, 0, 0

# Lists to store metrics
avg_sentence_length = []
percentage_of_complex_words = []
fog_index = []
complex_word_count = []
avg_syllable_word_count = []

# Iterate through each file in the directory
for file in os.listdir(text_dir):
    x, y, z, a, b = measure(file)
    avg_sentence_length.append(x)
    percentage_of_complex_words.append(y)
    fog_index.append(z)
    complex_word_count.append(a)
    avg_syllable_word_count.append(b)

# You can now analyze or print the results
import os
import re
from nltk.corpus import stopwords

# Directories
text_dir = "C:/Users/Nidhi Dhameliya/Desktop/jupyter/Data_Extraction_and_Text_Analysis_for_Blackcoffer_company/TitleText"
stopwords = set(stopwords.words('english'))

# Function to clean the text, remove stopwords and calculate word count & average word length
def cleaned_words(file):
    try:
        # Open file with 'utf-8' encoding to handle special characters
        with open(os.path.join(text_dir, file), 'r', encoding='utf-8') as f:
            text = f.read()
            # Remove punctuation
            text = re.sub(r'[^\w\s]', '', text)
            # Remove stopwords and split text into words
            words = [word for word in text.split() if word.lower() not in stopwords]
            # Calculate total length of words
            length = sum(len(word) for word in words)
            # Calculate average word length
            average_word_length = length / len(words) if len(words) > 0 else 0
        return len(words), average_word_length
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return 0, 0

# Lists to store results
word_count = []
average_word_length = []

# Iterate through each file in the directory
for file in os.listdir(text_dir):
    x, y = cleaned_words(file)
    word_count.append(x)
    average_word_length.append(y)

# Function to count personal pronouns in the text
def count_personal_pronouns(file):
    try:
        # Open file with 'utf-8' encoding to handle special characters
        with open(os.path.join(text_dir, file), 'r', encoding='utf-8') as f:
            text = f.read()
            # Define personal pronouns
            personal_pronouns = ["I", "we", "my", "ours", "us"]
            count = 0
            # Count occurrences of each pronoun
            for pronoun in personal_pronouns:
                count += len(re.findall(r"\b" + pronoun + r"\b", text))  # \b ensures whole word match
        return count
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return 0

# List to store personal pronouns count
pp_count = []

# Iterate through each file in the directory
for file in os.listdir(text_dir):
    x = count_personal_pronouns(file)
    pp_count.append(x)

# You can now analyze or print the results
import pandas as pd
import numpy as np

# Load the output dataframe
output_df = pd.read_excel('Output Data Structure.xlsx')

# Drop rows where URL_IDs 44, 57, and 144 do not exist
output_df.drop([44-37, 57-37, 144-37], axis=0, inplace=True)

# Define your variables (ensure these are already populated with data)
variables = [positive_score,
            negative_score,
            polarity_score,
            subjectivity_score,
            avg_sentence_length,
            percentage_of_complex_words,
            fog_index,
            avg_sentence_length,
            complex_word_count,
            word_count,
            avg_syllable_word_count,
            pp_count,
            average_word_length]

# Check the length of the dataframe and each variable
num_rows = len(output_df)  # Number of rows in the dataframe

for i, var in enumerate(variables):
    # Convert the variable to float and replace None with NaN
    var = [float(x) if x is not None else np.nan for x in var]
    
    # Ensure all variables match the number of rows in the dataframe
    if len(var) == num_rows:
        output_df.iloc[:, i + 2] = var
    elif len(var) < num_rows:
        # Pad with NaN if the variable is shorter
        var.extend([np.nan] * (num_rows - len(var)))
        output_df.iloc[:, i + 2] = var
    else:
        # Truncate if the variable is longer
        output_df.iloc[:, i + 2] = var[:num_rows]

# Save the dataframe to a CSV file
output_df.to_csv('Output_Data.csv', index=False)
