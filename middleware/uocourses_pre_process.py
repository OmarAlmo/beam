from bs4 import BeautifulSoup
import csv
import pandas as pd
import nltk
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import collections
import time
import math
import re

if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"
import middleware.utils as utils

STOP_WORDS = stopwords.words('english')
DICTIONARY = {}
INVERTED_INDEX = collections.defaultdict(list)

lemmatizer = WordNetLemmatizer()


class Node:
    def __init__(self, courseTitle=None, courseDesc=None):
        self.courseTitle = courseTitle
        self.courseDesc = courseDesc

def build_index_csv():
    with open ('./UofO_Courses.html') as html_file:
        soup = BeautifulSoup(html_file, 'html5lib')
    
    dictionary_file = open('./../uottawa_index.csv', 'w',newline='')
    dictionary = csv.writer(dictionary_file)
    dictionary.writerow(['DocID', 'Course Title', 'Course Description'])

    DocID = 0

    # Export to CVS
    for course in soup.find_all('div', class_='courseblock'):
        if course.find('p', class_='courseblocktitle noindent') == None:
            course_title = ""
        else:
            course_title = course.find('p', class_='courseblocktitle noindent').text
            course_title = " ".join(course_title.split())
            if ("3 crédits" in course_title) or ("è" in course_title):
                continue
        
        if course.find('p', class_='courseblockdesc noindent') == None:
            course_description = ""
        else:
            course_description = course.find('p', class_='courseblockdesc noindent').text
            course_description = " ".join(course_description.split())
            if ("3 crédits" in course_description) or ("é" in course_description):
	            continue
        
        dictionary.writerow([DocID, course_title, course_description])
	    
        DocID +=1
    dictionary_file.close()

def build_index():
	csvDataFile = open('./../uottawa_index.csv')
	csvReader = csv.reader(csvDataFile)

	i = 0
	for row in csvReader:
		if row==[]:
			continue
		title = row[0]
		description = row[1]
		newNode = Node(title, description)
		DICTIONARY[i] = newNode
		i+=1

	csvDataFile.close()
	return DICTIONARY

def bigram_helper(term):
    if any(char.isdigit() for char in term):
        return False
    if term in STOP_WORDS:
        return False
    if not term.isalpha():
        return False
    return True 

def build_bigram():
	index = pd.read_csv('./uottawa_index.csv', skiprows=0)
	bigramDictionary = collections.defaultdict(list)

	docID = 0
	for row in range(0, index.shape[0] - 1):
		try:
			title = index.iat[row,0]
		except:
			title = ""
		try:
			desc = index.iat[row, 1]
			if str(desc) == 'nan':
				desc = ""
		except:
			desc = ""
		print("TITLE:", title)
		print("DESC:", desc)
		text = title + desc
		print(text)
		tokenizedWords = word_tokenize(text)
		wordList = []
		for word in tokenizedWords:
			if bigram_helper(word):
				word = lemmatizer.lemmatize(word.lower())
				wordList.append(word)
		
			bigram = bigrams(wordList)
			print(docID)

			for i in bigram:
				bigramDictionary[i].append(docID)
			docID+=1

	uottawaBigramFile = open('./uottawa_bigram.csv', 'w')
	uottawaBigram = csv.writer(uottawaBigramFile)
	uottawaBigram.writerow(['id','bigram', 'docIDs'])

	id = 0
	for key in bigramDictionary:
		uottawaBigram.writerow([id, [key[0],key[1]], bigramDictionary[key]])
		print(id)
		id += 1

	uottawaBigramFile.close()

def build_dictionary():
	csvDataFile = open('./../uottawa_index.csv')
	csvReader = csv.reader(csvDataFile)

	for row in csvReader:
		if row==[]:
			continue
		try:
			i = int(row[0])
		except:
			i = row[0]

		title = row[1]
		description = row[2]
		row_words = title + description

		# Tokenize words
		tokenized_words = word_tokenize(row_words)

		for word in tokenized_words:
			# Lemmatize & fold case words		
			word = lemmatizer.lemmatize(word.lower())

			if word in STOP_WORDS:
				continue
			
			flag=True

			for kw in INVERTED_INDEX[word] :
				if kw[0] == i :
					kw[1]=kw[1]+1
					flag=False
			if flag:
				INVERTED_INDEX[word].append([i,1])

	csvDataFile.close()
	return INVERTED_INDEX


def export_dictionary_csv(inverted_index):
	inverted_csv_file = open('./../uottawa_dictionary.csv', 'w',newline='')
	csv_writer = csv.writer(inverted_csv_file)
	csv_writer.writerow(['Term', 'DocID&Sequence'])
	for key in inverted_index:
		csv_writer.writerow([key, inverted_index[key]])
	inverted_csv_file.close()

def add_tfidf():
	tfidf_file = open('./../tfidf_uottawa.csv', 'w')
	csv_writer = csv.writer(tfidf_file)
	csv_writer.writerow(['ID','Term', 'DocID/TF-IDF'])

	df = pd.read_csv("./../inverted_index.csv", skiprows=0)
	counter = 0

	for i in range(0, df.shape[0]-1):
		term = df.iloc[i]['Term']
		docIDSeq = utils.convert_to_list(df.iloc[i]['DocID&Sequence'])
		s = []
		for j in docIDSeq:
			docID = int(j[0])
			print("TERM:",term)
			tfidf = utils.calculate_tfidf(term, docID)
			tmp = [docID, tfidf]
			s.append(tmp)
		csv_writer.writerow([counter,term, s])
		counter+= 1
		print(s)
		
	tfidf_file.close()

def main():
	build_index_csv()
	dictionary = build_dictionary()
	export_dictionary_csv(dictionary)
	add_tfidf()