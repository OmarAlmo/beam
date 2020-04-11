
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"
import middleware.utils as utils

import csv, re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pythonds.basic.stack import Stack


OPERATORS = ['AND', 'OR', 'AND_NOT', '(', ')']
PRECIDENT = {
    '(': 1,
    'AND': 2,
    'OR': 2,
    'NOT': 2,
    'AND_NOT': 2,
}
PUNCUATIONS = [',', '[', ']', '']
INDEX_REGEX = r'(\[\d+, \d+\])'
lemmatizer = WordNetLemmatizer()

LEMMATIZE = True
NORMALIZE = True


def infix_to_postfix(query):
    query_list = word_tokenize(query)

    stack = Stack()
    postfix = []

    for word in query_list:
        if word not in OPERATORS:
            postfix.append(word)
        elif word == '(':
            stack.push(word)
        elif word == ')':
            top = stack.pop()
            while top != '(':
                postfix.append(top)
                top = stack.pop()
        else:
            while not stack.isEmpty() and PRECIDENT[
                    stack.peek()] >= PRECIDENT[word]:
                postfix.append(stack.pop())
            stack.push(word)

    while not stack.isEmpty():
        postfix.append(stack.pop())
    return ' '.join(postfix)


def process_postfix(corpus,postfix, globalexpansion):
    '''
	input: postfix query
	output: list of docIDs of query
	'''
    postfix_list = word_tokenize(postfix)
    stack = Stack()
    output = []
    for word in postfix_list:
        if word not in OPERATORS:
            stack.push(word)
        else:
            a = stack.pop()
            b = stack.pop()
            op = word
            res = boolean_retrieval(corpus,a, b, op, globalexpansion)
            output = res
            stack.push(res)

    return output

def get_docs_ids(corpus,word):
    if corpus == 'uottawa':
        df = pd.read_csv("./uottawa_dictionary.csv", header=0)
    else:
        df = pd.read_csv("./reuters_dictionary.csv", header=0)

    wildcard = False

    if '*' in word:
        wildcard = True


    if LEMMATIZE:
        word = lemmatizer.lemmatize(word)
    if NORMALIZE:
        word = word.lower()

    output = []

    if wildcard:
        regx = re.compile(wildcard_to_regex(word))
        query = "re.match(regx, df.iloc[i]['Term'])"
        pass
    else:
        row = utils.get_term_docIDSeq(corpus, word)

        for i in row:
            output.append(i[0])

    return output


def boolean_retrieval(corpus,a, b, op, globalexpansion):

    if type(a) != list:
        listA = get_docs_ids(corpus,a)
        if globalexpansion: 
            synA = utils.get_synonym(a)
            print("synonyms added for",a, ":")
            try: 
                t1 = get_docs_ids(synA[0]) 
                listA += t1
                print("1st synonym",synA[0])
            except: pass
            try: 
                t2 = get_docs_ids(synA[1]) 
                listA += t2
                print("2nd synonym",synA[1])
            except: pass        
    else:
        listA = a

    if type(b) != list:
        listB = get_docs_ids(corpus,b)
        if globalexpansion: 
            synB = utils.get_synonym(b)
            print("synonyms added for",b, ":")
            try: 
                t1 = get_docs_ids(synB[0]) 
                listB += t1
                print("1st synonym",synB[0])
            except: pass
            try: 
                t2 = get_docs_ids(synB[1]) 
                listB += t2
                print("2nd synonym",synB[1])
            except: pass
    else:
        listB = b

    if op == 'AND':
        res = list(set(listA).intersection(listB))
    elif op == 'OR':
        res = list(set(listA).union(set(listB)))
    else:  # op == 'AND_NOT':
        res = list(set(listA) - set(listB))

    return res

def wildcard_to_regex(wildcard_word):
    w = list(wildcard_word)
    out = ""
    for c in w:
        if c == '*':
            c = '(.' + c + ')'
        out += c
    return out


def main(corpus, query, globalexpansion, topic):

    if len(query.split()) < 2:
        ids = get_docs_ids(corpus,query)
        documents = utils.retrieve_documents(corpus,ids[:15])
        
    else:
        postfixquery = infix_to_postfix(query)
        ids = process_postfix(corpus,postfixquery,globalexpansion)
        if corpus == 'reuters': filteredIDs = utils.filter_documents_topic(ids, topic, 'boolean')
        else: filteredIDs = ids
        documents = utils.retrieve_documents(corpus,filteredIDs[:15])
        if documents == []:
            return [["No documents with that query."]]
    return documents
