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

def retrieve_documents(corpus, id_list):
    output = []
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_index.csv')
        for i in id_list:
            # [0title, 1desc, 2docID]
            tmp = [df.iat[int(i), 1], df.iat[int(i), 2], df.iat[int(i), 0]]
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

def get_term_docIDSeq(corpus, term):
    if corpus == 'uottawa':
        df = pd.read_csv("./uottawa_dictionary.csv", index_col=0)
    else:
        df = pd.read_csv('./reuters_dictionary.csv', index_col=0)

    for i in range(df.shape[0]):
        if term == df.iat[i,0]:
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

def get_bigramDict_by_word(corpus,keyword):
    bigramDict={}
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_bigram.csv')
    else:
        df = pd.read_csv('./reuters_bigram.csv')
    
    for i in range(0, df.shape[0]):
        bigram = df.iat[i,1]
        bigramList = ast.literal_eval(bigram)
        bigram2 = df.iat[i,2]
        print(bigram2)
        bigramList2 = ast.literal_eval(bigram2)
        t1 = bigramList[0]
        if(t1==keyword):
            bigramDict[bigram]=[bigramList[1],len(bigramList2)]
    return bigramDict


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

    sortedOutput = {key: value for (key, value) in sorted(output.items())}
    print("sortedOutput:", sortedOutput)
    res = []
    for syn in sortedOutput:
        res.append(syn.name().split('.')[0])

    res = list(dict.fromkeys(res))
    res.remove(term)
    return res

# print("get(synonyms('wheat'))")
# print(get_synonym('wheat'))

# print("get_synonym('bank'))")
# print(get_synonym('bank'))

# print("get_synonym('coffee')")
# print(get_synonym('coffee'))

# print("get_synonym('stock')")
# print(get_synonym('stock'))

# print("get_synonym('oil'))")
# print(get_synonym('oil'))


def filter_documents_topic(ids,topic, model):
    if topic == 'all':
        return ids
    
    df = pd.read_csv('./reuters_index.csv', index_col=0)
    if model == 'vsm':
        res = {}
        i = 0;
        for k, v in ids.items():
            if df.iat[int(k),1] == topic:
                res[k] = v
        return res
    else:
        res = []
        for i in ids:
            if df.iat[int(i),1] == topic:
                res.append(i)
        return res
