import pandas as pd
import numpy as np
import re
import string
import nltk

import pandas as pd

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

STOP_WORDS = stopwords.words()


EMOJI_PATTERN = re.compile("["
                           u"\U0001F600-\U0001F64F"  
                           u"\U0001F300-\U0001F5FF"  
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"  
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)


def cleaning(text):
    
    text = text.lower()
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('[’“”…]', '', text)

    text = EMOJI_PATTERN.sub(r'', text)


    text_tokens = word_tokenize(text)
    tokens_without_sw = [
        word for word in text_tokens if not word in STOP_WORDS]
    filtered_sentence = (" ").join(tokens_without_sw)
    text = filtered_sentence

    return text


def frequent_in_reviews(a):
    df = pd.read_csv(f"{a}") 
    dt = df['title'].astype(str).apply(cleaning)

    word_count = Counter(" ".join(dt).split()).most_common(10)
    word_frequency = pd.DataFrame(word_count, columns = ['Word', 'Frequency'])
    word_frequency.to_csv("reviews_frequent.csv")

def popular_reviews(a):
  df = pd.read_csv(f"{a}", index_col=[0])
  sorted_df = df.sort_values(by='people_rate', ascending=False, ignore_index=True)
  sorted_df.to_csv("popular_reviews.csv")


def reviews_sentinment(a):
    df = pd.read_csv(f"{a}") 
    df['sentiment'] = np.where(df['rating'] >= 5.0, 1,
                           np.where(df['rating'] >= 4.0, 1, 0))
    df.to_csv("reviews_sentiment.csv")


def popular_products(a):
  df = pd.read_csv(f"{a}", index_col=[0])
  sorted_df = df.sort_values(by='rating_count', ascending=False, ignore_index=True)
  sorted_df.to_csv("popular_products.csv")


def products_sentinment(a):
    df = pd.read_csv(f"{a}") 
    df['sentiment'] = np.where(df['rating'] >= 5.0, 1,
                           np.where(df['rating'] >= 4.0, 1, 0))
    df.to_csv("produts_sentiment.csv")


def frequent_in_products(a):
    df = pd.read_csv(f"{a}") 
    dt = df['title'].astype(str).apply(cleaning)

    word_count = Counter(" ".join(dt).split()).most_common(10)
    word_frequency = pd.DataFrame(word_count, columns = ['Word', 'Frequency'])
    word_frequency.to_csv("products_frequent.csv")





