if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"

from bs4 import BeautifulSoup
import csv
import pandas as pd
from dotenv import load_dotenv
import sys, os, glob
import middleware.utils as utils

import nltk
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
import collections
import ast

loadEnv = load_dotenv('./.env')
reutersDir = os.getenv('reuters_dir')

csv.field_size_limit(sys.maxsize)

STOP_WORDS = stopwords.words('english')
DICTIONARY = collections.defaultdict(list)
lemmatizer = WordNetLemmatizer()


def remove_tags(s):
    slist = s.split()
    res = []
    for i in slist:
        if i[0] == '<':
            pass
        else:
            res.append(i)
    return ' '.join(res)


def valid_term(term):
    if any(char.isdigit() for char in term):
        return False
    if term in STOP_WORDS:
        return False
    if not term.isalpha():
        return False
    if len(term) < 3:
        return False
    return True


def build_index():
    retuersIndexFile = open('./reuters_index.csv', 'w')
    retuersIndex = csv.writer(retuersIndexFile)
    retuersIndex.writerow(['docID', 'title', 'topics','author', 'date', 'body', 'topics'])
    docID = 0
    for file in glob.glob(os.path.join(reutersDir, '*.sgm')):
        print(file)
        f = open(file, 'rb')
        data = f.read()
        soup = BeautifulSoup(data, 'html.parser')

        for article in soup.findAll('reuters'):

            try:
                title = remove_tags(article.find('title').text)
            except:
                title = 'N/A'

            date = article.find('date').text

            try:
                body = article.find('body').text
                body = body.rsplit(' ',
                                   1)[0]  # removes Reuters last word of text
                body = " ".join(body.split())
            except:
                body = None

            try:
                author = article.find('author').text.strip()
            except:
                author = 'N/A'

            try:
                topics = article.find('topics').text
            except:
                topics = 'N/A'

            if (body != None):
                retuersIndex.writerow(
                    [docID, title, topics, author, date, body])
                docID += 1
    
    f.close()
    retuersIndexFile.close()

def bigram_helper(term):
    if any(char.isdigit() for char in term):
        return False
    if term in STOP_WORDS:
        return False
    if not term.isalpha():
        return False
    return True 

def build_bigram():
    index = pd.read_csv('./reuters_index.csv', header=0)
    bigramDictionary = collections.defaultdict(list)

    for row in range(0, index.shape[0]):
        docID = int(index.iat[row, 0])
        body = index.iat[row, 5]

        tokenizedWords = word_tokenize(body)
        wordList = []
        for word in tokenizedWords:
            if bigram_helper(word):
                word = lemmatizer.lemmatize(word.lower())
                wordList.append(word)
        bigram = bigrams(wordList)
        print(docID)
        for i in bigram:
            bigramDictionary[i].append(docID)

    reutersBigramFile = open('./reuters_bigram.csv', 'w')
    retuersBigram = csv.writer(reutersBigramFile)
    retuersBigram.writerow(['id','bigram', 'docIDs'])

    id = 0
    for key in bigramDictionary:
        if (len(bigramDictionary[key]) > 4):
            retuersBigram.writerow([id, [key[0],key[1]], bigramDictionary[key]])
            print(id)
            id += 1

    reutersBigramFile.close()

def reduce_bigram():
    df = pd.read_csv('./reuters_bigram.csv', index_col=0, header=0)
    # df = df[len(ast.literal_eval(df.docIDs)) < 5]
    for i in range(0,df.shape[0]-1):
        lenDocIDs = len(ast.literal_eval(df.iat[i,1]))
        if lenDocIDs < 5:
            df.drop(df.index[i])
            print("dropeed")
    df.to_csv('reuters_bigram_2.csv')

def build_dictionary():
    index = pd.read_csv('./reuters_index.csv', header=0)

    for row in range(0, index.shape[0] - 1):
        try:
            docID = int(index.iat[row, 0])
        except:
            docID = index.iat[row, 0]
        # title
        title = index.iat[row, 1]

        #author
        if type(index.iat[row, 3]) == str:
            author = index.iat[row, 3]
        else:
            author = ''

        #body
        body = index.iat[row, 5]
        print("TITLE", title)

        rowWords = title + author + body
        tokenizedWords = word_tokenize(rowWords)

        for word in tokenizedWords:
            word = lemmatizer.lemmatize(word.lower())

            if word in STOP_WORDS:
                pass

            else:
                flag = True

                for kw in DICTIONARY[word]:
                    if kw[0] == docID:
                        kw[1] = kw[1] + 1
                        flag = False
                if flag:
                    DICTIONARY[word].append([docID, 1])
                print(docID)
    return DICTIONARY

def export_dictionary():
    retuersDictionaryFile = open('./reuters_dictionary.csv', 'w')
    retuersDictionary = csv.writer(retuersDictionaryFile)
    retuersDictionary.writerow(['id', 'term', 'freq&sequence'])
    id = 0
    for key in DICTIONARY:
        retuersDictionary.writerow([id, key, DICTIONARY[key]])
        id += 1
    retuersDictionaryFile.close()


'''
input dictionary file (csv)
output dictionary csv with terms have have df of >5
'''
def remove_low_freq_terms():
    dictionaryFile = open('./../reuters_dictionary.csv', 'r')
    dictionary = csv.reader(dictionaryFile)

    retuersDictionaryFile = open('./../reduced_reuters_dictionary.csv', 'w')
    retuersDictionary = csv.writer(retuersDictionaryFile)
    retuersDictionary.writerow(['term','docFrequency', 'freq&sequence'])
    for row in dictionary:
        term = row[1]
        if valid_term(term):
            termList = utils.convert_to_list(row[2])

            if len(termList) < 4:
                pass
            else:
                retuersDictionary.writerow([term,len(termList), row[2]])

    dictionaryFile.close()
    retuersDictionaryFile.close()

def add_tfidf():
    tfidf_file = open('./../tfidf_reuters__2.csv', 'w')
    csv_writer = csv.writer(tfidf_file)
    csv_writer.writerow(['ID', 'Term', 'DocID/TF-IDF'])

    df = pd.read_csv("./../reduced_reuters_dictionary.csv", skiprows=0)

    counter = 0

    for i in range(0, df.shape[0] - 1):
        term = df.iat[i, 0]
        docFreq = df.iat[i,1]
        docIDSeq = utils.convert_to_list(df.iat[i, 2])
        print("TERM", term)

        s = []
        for j in docIDSeq:
            docID = int(j[0])
            termFreq = int(j[1])

            tfidf = utils.calculate_tfidf('reuters', term, docID, docFreq, termFreq)
            tmp = [docID, tfidf]
            s.append(tmp)
        csv_writer.writerow([counter, term, s])
        counter += 1
        print(s)
    tfidf_file.close()



def generate_letter_bigram():
    df = pd.read_csv('./reuters_dictionary.csv')
    output = {}
    for i in range(df.shape[0]):
        termID = df.iat[i,0]
        term = '$'+str(df.iat[i,1])+'$'

        # letter gram 
        tmp = list(nltk.trigrams(term))
        
        for g in tmp:
            gram = "".join(g)
            try: output[gram] += [termID]
            except: output[gram] = [termID]
    
    letterGramFile = open('./reuters_letter_gram.csv', 'w')
    letterGram = csv.writer(letterGramFile)
    letterGram.writerow(['id', 'gram', 'termID'])
    id = 0
    for k, v in output.items():
        letterGram.writerow([id, k, v])
        id += 1

    letterGramFile.close()
