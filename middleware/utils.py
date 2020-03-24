import csv
import pandas as pd
import re
import math
import ast

TFIDF_INDEX_REGEX = r'\[\d+, [+-]?[0-9]*[.]?[0-9]+\]'
PLAIN_INDEX_REGEX = r'(\[\d+, \d+\])'

UOTTAWA_NUMBER_DOCUMENTS = 612 #pd.read_csv('./../uottawa_index.csv').shape[0] - 1
REUTERS_NUMBER_DOCUMENTS = 19042 #pd.read_csv('./../reuters_index.csv').shape[0] - 1


def retrieve_documents(corpus, id_list):
    output = []
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_index.csv')
        for i in id_list:
            # [0title, 1desc]
            tmp = [df.iat[int(i), 0], df.iat[int(i), 1]]
            output.append(tmp)
    else:
        df = pd.read_csv('./reuters_index.csv', index_col=0)
        for i in id_list:
            # [1title, 2topics, 3author, 4date, 5body])
            tmp = [
                df.iat[int(i), 1], df.iat[int(i), 2], df.iat[int(i), 3],
                df.iat[int(i), 4], df.iat[int(i), 5]
            ]
            output.append(tmp)
    return output


def get_document(corpus, i):
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_index.csv', header=0, index_col=0)

        title = df.iat[i, 0]
        desc = df.iat[i, 1]

        if type(title) != str:
            title = ""
        if type(desc) != str:
            desc = ""

        return title + desc

    else:
        df = pd.read_csv('./reuters_index.csv', header=0, index_col=0)

        title = df.iat[i, 0]
        body = df.iat[i, 3]

        return title + body


def get_term_docIDSeq(corpus, term):
    if corpus == 'uottawa':
        df = pd.read_csv("./uottawa_tfidf.csv", index_col=0)
        j = 1
    else:
        df = pd.read_csv('./reuters_tfidf.csv', index_col=0)
        j = 2

    for i in range(0, df.shape[0] - 1):
        if term == df.iloc[i]['term']:
            row = df.iat[i, j]
            p = re.compile(PLAIN_INDEX_REGEX)
            index_list = p.findall(row)
    return [i[1:-1].split(', ') for i in index_list]


def convert_to_list(line):
    p = re.compile(TFIDF_INDEX_REGEX)
    return [i[1:-1].split(', ') for i in p.findall(line)]


def get_tf(corpus, term, docID):
    doc = get_document(corpus, docID)
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
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_tfidf.csv')
        return df.loc[df['Term'] == term]['tfidf'].values
    else:
        df = pd.read_csv('./reuters_tfidf.csv')
        return df.loc[df['Term'] == term]['tfidf'].values

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
