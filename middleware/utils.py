import csv
import pandas as pd
import re
import math
import ast
import nltk
from nltk.corpus import wordnet, brown
import collections


TFIDF_INDEX_REGEX = r'\[\d+, [+-]?[0-9]*[.]?[0-9]+\]'
PLAIN_INDEX_REGEX = r'(\[\d+, \d+\])'

UOTTAWA_NUMBER_DOCUMENTS = 612 #pd.read_csv('./../uottawa_index.csv').shape[0] - 1
REUTERS_NUMBER_DOCUMENTS = 19042 #pd.read_csv('./../reuters_index.csv').shape[0] - 1

# Relevnace format: {q:DocIDS}
RELEVANT_DOCS = collections.defaultdict(list)
NRELEVANT_DOCS = collections.defaultdict(list)

# RELEVANT_DOCS = {'canada': ['16135']}
# NRELEVANT_DOCS = {'canada': ['4065']}

def retrieve_documents(corpus, id_list):
    output = []
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_index.csv', index_col=0)
        for i in id_list:
            # [0title, 1desc]
            tmp = [df.iat[int(i), 0], df.iat[int(i), 1]]
            output.append(tmp)
    else:
        df = pd.read_csv('./reuters_index.csv')
        for i in id_list:
            # [0title, 1topics, 2author, 3date, 4body, 5docID])
            tmp = [
                df.iat[int(i), 1], df.iat[int(i), 2], df.iat[int(i), 3],
                df.iat[int(i), 4], df.iat[int(i), 5], df.iat[int(i), 0]
            ]
            output.append(tmp)
    return output


def get_document_content(corpus, docID):
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_index.csv', header=0, index_col=0)

        title = df.iat[docID, 0]
        desc = df.iat[docID, 1]

        if type(title) != str:
            title = ""
        if type(desc) != str:
            desc = ""

        return title + desc

    else:
        df = pd.read_csv('./reuters_index.csv', header=0, index_col=0)

        title = df.iat[docID, 0]
        body = df.iat[docID, 4]
        return title + body
        # return df.iat[docID, 4]


def get_term_docIDSeq(corpus, term):
    if corpus == 'uottawa':
        df = pd.read_csv("./uottawa_dictionary.csv", index_col=0)
    else:
        df = pd.read_csv('./reuters_dictionary.csv', index_col=0)

    for i in range(0, df.shape[0] - 1):
        if term == df.iloc[i]['Term']:
            row = df.iat[i, 1]
            p = re.compile(TFIDF_INDEX_REGEX)
            index_list = p.findall(row)
            return [j[1:-1].split(', ') for j in index_list]
    return[]

def convert_to_list(line):
    p = re.compile(TFIDF_INDEX_REGEX)
    return [i[1:-1].split(', ') for i in p.findall(line)]

def get_tf(corpus, term, docID):
    doc = get_document_content(corpus, docID)
    row = get_term_docIDSeq(corpus, term)
    try:
        for i in row:
            if (int(i[0]) == docID):
                return float(i[1]) / float(len(doc))
    except:
        return 0

def get_df(corpus, term):
    return len(get_term_docIDSeq(corpus, term))


def get_idf(corpus, term):
    if corpus == 'uottawa':
        return math.log10(UOTTAWA_NUMBER_DOCUMENTS /
                          (get_df(corpus, term) + 1))
    return math.log10(REUTERS_NUMBER_DOCUMENTS / (get_df(corpus, term) + 1))

def calculate_tfidf(corpus, term, docID):
    return get_tf(corpus, term, docID) * get_idf(corpus, term)

def get_tfidf(corpus, term, docID):
    row = get_term_docIDSeq(corpus, term)
    for elem in row:
        if elem[0] == str(docID):
            return elem[1]
    return 0

def get_bigram(corpus,term):
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_bigram.csv')
    else:
        df = pd.read_csv('./reuters_bigram.csv')
    
    for i in range(0, df.shape[0]):
        bigram = df.iat[i,1]
        bigramList = ast.literal_eval(bigram)
        t1 = bigramList[0]
        t2 = bigramList[1]

# def get_synonym(term):
#     synonyms = set()
#     for syn in wordnet.synsets(term):
#         for l in syn.lemmas():
#             synonyms.add(l.name())
#     res = []
#     for i in list(synonyms):
#         if '-' in i or '_' in i or i == term: pass 
#         else: res.append(i)
#     return res

def get_synonym(term):
    t1 = wordnet.synset(wordnet.synsets(term)[0].name())

    synonyms = []
    for syn in wordnet.synsets(term):
        synonyms.append(syn.name())

    output = {}
    for i in synonyms:
        t2 = wordnet.synset(i)
        sim = t1.wup_similarity(t2)
        output[t2] = sim

    sortedOutput = {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)}
    
    res = []
    for syn in sortedOutput:
        res.append(syn.name().split('.')[0])

    res = list(dict.fromkeys(res))
    res.remove(term)
    return res