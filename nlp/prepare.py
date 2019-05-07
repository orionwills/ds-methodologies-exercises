import unicodedata
import re
import json
from functools import reduce
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd
import acquire_codeup_blog

# Michael/Zach's pipe function that allows you to pipe functions
def pipe(v, *fns):
    return reduce(lambda x, f: f(x), fns, v)

# Master function for cleaning
def basic_clean(text):
    return pipe(text, lowercase_text, normalize_text, remove_special)
# Lowercase all text
def lowercase_text(text):    
    return text.lower()
# Normalize, encode, and decode
def normalize_text(text):
    return unicodedata.normalize('NFKD', text)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
# Remove special characters
def remove_special(text):
    return re.sub(r"[^a-z0-9'\s]", '', text)

# NLP Stuff
# Tokenize and return dictionary
def tokenize(text):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(text, return_str=True)
# Stem and return dictionary
def stem(text):
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in text.split()]
    return ' '.join(stems)
# Lemmatize and return dictionary
def lemmatize(text):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    return ' '.join(lemmas)
# Remove stopwords, accepts words to add or remove from the master stopword list
def remove_stopwords(text, include=[], exclude=[]):
    stopword_list = stopwords.words('english')
    # add in new stopwords
    stopword_list.extend(include)
    # remove stopwords
    for word in exclude:
        stopword_list.remove(word)
    
    words = text.split()
    filtered_words = [w for w in words if w not in stopword_list]
    return ' '.join(filtered_words)

# Article preparation - calls all above functions
def prep_article(dictionary):
    
    clean_stem = pipe(dictionary['Article'],
                      basic_clean,
                      tokenize,
                      remove_stopwords,
                      stem)
    
    clean_lemm = pipe(dictionary['Article'],
                      basic_clean,
                      tokenize,
                      remove_stopwords,
                      lemmatize)
       
    new_dict = {
        'title': dictionary['Title'].lower(),
        'category': dictionary['Category'].lower(),
        'original': dictionary['Article'].lower(),
        'stemmed': stem(dictionary['Article']),
        'lemmatized': lemmatize(dictionary['Article']),
        'clean_stem': clean_stem,
        'clean_lemm': clean_lemm
    }
    return new_dict

# All article preparation
def prep_article_data(dict_list):
    cleaned_dict_list = [prep_article(d) for d in dict_list]
    return cleaned_dict_list