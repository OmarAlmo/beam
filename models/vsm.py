if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"
import middleware.utils as utils

import csv
import pandas as pd
import math
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import difflib
import  collections
import collections
import re

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"
import middleware.utils as utils

lemmatizer = WordNetLemmatizer()

CUSTOM_STOP_WORDS = ['course', 'knowledge', 'business', 'effectively','student','constitutes','introduce','major','minor', '(', ')', ',', '"','.', ';']
NLTK_WORDS = stopwords.words('english')
STOP_WORDS = CUSTOM_STOP_WORDS + NLTK_WORDS
PUNCUATIONS = [',', '[', ']', '', ':']

def process_query(query):
    '''
    input: query
    output: tokenized list of query with removed stop words and lemmatized & lower case words
    '''
    output = []
    query_list = word_tokenize(query)

    for word in query_list:
        if word in STOP_WORDS:
            continue
        else:
            word = lemmatizer.lemmatize(word.lower())
            output.append(word)
    return output


def measure_scores(corpus,query):
    scores = collections.defaultdict(list)
    for term in query:
        row = utils.get_term_docIDSeq(corpus,term)
        for i in row:
            docID = i[0]
            tfidf = i[1]
            if docID in scores.keys():
                scores[docID] += float(tfidf)
            else:
                scores[docID] = float(tfidf)
    return scores


def calculate_ranking(scores):
    sorted_ranking = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
    ids = []
    for k, v in sorted_ranking.items():
        ids.append(k)
    return ids

def main(corpus,query):
    query_list = process_query(query)
    scores = measure_scores(corpus,query_list)
    ids_ranking = calculate_ranking(scores)
    return utils.retrieve_documents(corpus,ids_ranking[:15])

