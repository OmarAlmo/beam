import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import collections

import csv

import json

df = pd.read_csv("./corpus/parsed_UofO_Courses.csv")
lemmatizer = WordNetLemmatizer()

NUMBER_OF_ROWS = df.shape[0]

CUSTOM_STOP_WORDS = ['course', 'knowledge', 'business', 'effectively','student','constitutes','introduce','major','minor', '(', ')', ',', '"','.', ';']
NLTK_WORDS = stopwords.words('english') + stopwords.words('french')
STOP_WORDS = CUSTOM_STOP_WORDS + NLTK_WORDS

DICTIONARY = {}
INVERTED_INDEX = collections.defaultdict(list)

class Node:
    def __init__(self, courseTitle=None, courseDesc=None):
        self.courseTitle = courseTitle
        self.courseDesc = courseDesc
	
def build_dictionary():
	csvDataFile = open('./corpus/parsed_UofO_Courses.csv')
	csvReader = csv.reader(csvDataFile)

	i = 0
	for row in csvReader:
		title = row[0]
		description = row[1]
		newNode = Node(title, description)
		DICTIONARY[i] = newNode
		i+=1

	csvDataFile.close()


def build_index():
	csvDataFile = open('dictionary.csv')
	csvReader = csv.reader(csvDataFile)

	i = 1

	for row in csvReader:
		title = row[0]
		description = row[1]
		row_words = title + description

		# Tokenize words
		tokenized_words = word_tokenize(row_words)

		for word in tokenized_words:
			# Lemmatize & fold case words
			word = word.lower()			
			word = lemmatizer.lemmatize(word)

			if word in STOP_WORDS:
				continue
			
			flag=True

			for kw in INVERTED_INDEX[word] :
				if kw[0] == i :
					kw[1]=kw[1]+1
					flag=False
			if flag:
				INVERTED_INDEX[word].append([i,1])
		i+=1
	csvDataFile.close()

def build_indeverted_csv():
	inverted_csv_file = open('inverted_index.csv', 'w')
	csv_writer = csv.writer(inverted_csv_file)
	csv_writer.writerow(['Term', 'DocID&Sequence'])
	for key in INVERTED_INDEX:
		csv_writer.writerow([key, INVERTED_INDEX[key]])
	inverted_csv_file.close()
	
build_index()
build_indeverted_csv()

