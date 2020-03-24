import csv
import pandas as pd
import  collections
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import math
import difflib
import Levenshtein

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"
import middleware.utils as utils
import middleware.pre_process as pre_process

dictionary=pre_process.build_dictionary()
inverted_dictionary= pre_process.build_inverted_index()
vector_dictionary=collections.defaultdict(list)

lemmatizer = WordNetLemmatizer()

CUSTOM_STOP_WORDS = ['course', 'knowledge', 'business', 'effectively','student','constitutes','introduce','major','minor', '(', ')', ',', '"','.', ';']
NLTK_WORDS = stopwords.words('english')
STOP_WORDS = CUSTOM_STOP_WORDS + NLTK_WORDS

# take a query string and generate it into a tokenized lemmatized query list'''
def generate_query(query):
	queryList=[]

	# Tokenize words
	tokenized_words = word_tokenize(query)

	for word in tokenized_words:
		# Lemmatize & fold case words
		word = lemmatizer.lemmatize(word)
		word = word.lower()
		
		if word in STOP_WORDS:
				continue
		if word in queryList:
				continue
		queryList.append(word_check(word))
	return queryList

def word_check(word):
	index_file = open('inverted_index.csv', 'r')
	index = csv.reader(index_file)
	
	document_words = []
	for i in index:
		document_words.append(i[0])
	
	# returns closes match if word not in index
	if word not in document_words:
		matches = difflib.get_close_matches(word, document_words)
	else: 
		return word
	
	min_distance = Levenshtein.distance(word, matches[0])

	for m in matches:
		if Levenshtein.distance(word, m) <= min_distance:
			word = m
			min_distance = Levenshtein.distance(word, m)	
	index_file.close()

	print("****** \n WORD CORRECTION: ", word, "\n******")
	return word

# building vector matrix with tf-idf value
def make_Vectormatrix(queryList):
	vector_dictionary=collections.defaultdict(list)
	#Initialise vector with 0's
	totalNum_document = len(dictionary)
	for query_element in queryList:
			vector_dictionary[query_element]=[0] * totalNum_document
	for word in inverted_dictionary:
		if word in vector_dictionary:
			for x in inverted_dictionary[word]:
				vector_dictionary[word][x[0]-1]=x[1]
		else:
			continue

	#make the dictionary to be tf-idf
	for term in vector_dictionary:
		if(len(inverted_dictionary[term])==0):
			idf=0
		else:
			idf=math.log((totalNum_document+1)/len(inverted_dictionary[term]))
		for i in range(0,len(vector_dictionary[term])):
			vector_dictionary[term][i]=vector_dictionary[term][i]*idf
	return vector_dictionary

# calculate the score and build a sorted score table in format of [docID:score]
def make_scoreTable(vector_dictionary):
	scoreTable=collections.defaultdict(list)
	#docID=0
	for i in range(0,len(dictionary)):
		score=0
		for x in vector_dictionary:
			score+=vector_dictionary[x][i-1]
		scoreTable[i]=score
	#remove the document with score 0
	zero_score=[]
	for doc in scoreTable:
		if scoreTable[doc]==0:
			zero_score.append(doc)
	for x in zero_score:
		scoreTable.pop(x)
	return sorted(scoreTable.items(), key=lambda x: x[1],reverse=True) 

# extract the docID from score table
def make_idList(scoreTable):
	idList=[]
	for x in scoreTable:
		idList.append(x[0])
	return idList

        
def main(query):
	queryList=generate_query(query)
	matrix=make_Vectormatrix(queryList)
	scoreTable=make_scoreTable(matrix)
	idList=make_idList(scoreTable)
	documents = utils.retrieve_documents(idList)
	return documents