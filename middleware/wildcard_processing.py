if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"

from dotenv import load_dotenv
import sys, os, glob

import nltk
import pandas as pd
import numpy as np
import csv
from difflib import SequenceMatcher
from itertools import islice 


def process_wildcard(corpus, term):
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_letter_gram.csv', index_col=0)
    else:
        df = pd.read_csv('./reuters_letter_gram.csv', index_col=0)
    
    tmp = list(nltk.trigrams(term.replace('*','$')))
    
    newTermGrams = []
    for g in tmp:
        newTermGrams.append("".join(g))
    res = set()
    for i in range(df.shape[0]):
        gram = df.iat[i,0]
        if gram in newTermGrams: 
            tmp = df.iat[i,1].strip('][').split(', ')
            for i in tmp:
                res.add(i)
    
    return res

def most_prob_term(corpus, term):
    termList = process_wildcard(corpus, term)

    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_dictionary.csv', index_col=0)
    else:
        df = pd.read_csv('./reuters_dictionary.csv', index_col=0)
    
    scores = {}
    for i in termList:
        dicTerm = df.iat[int(i),0]
        simScore = SequenceMatcher(None, term, dicTerm).ratio()
        scores[i] = simScore
    

    sortedScores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}

    for k in sortedScores.keys():
        w = df.iat[int(k), 0]
        if len(w) > len(term):
            return w

    newTerm = df.iat[int(next(iter(sortedScores))), 0]
    return newTerm
    