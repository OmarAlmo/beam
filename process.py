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
NLTK_WORDS = stopwords.words('english')
STOP_WORDS = CUSTOM_STOP_WORDS + NLTK_WORDS

DICTIONARY = {}
INVERTED_INDEX = collections.defaultdict(list)

# lancaster=LancasterStemmer()

class Node:
    def __init__(self, courseTitle=None, courseDesc=None):
        self.courseTitle = courseTitle
        self.courseDesc = courseDesc

# class IndexNode:
# 	def __init__(self, valList):
# 		self.valList = []

def tokenize_row(row):
	title = word_tokenize(row[0]) #row[0] = title
	desc = word_tokenize(row[1]) #row[1] = desctription
	
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
	csvDataFile = open('./corpus/parsed_UofO_Courses.csv')
	csvReader = csv.reader(csvDataFile)

	i = 0

	for row in csvReader:
		title = row[0]
		description = row[1]
		row_words = title + description

		# Tokenize words
		tokenized_words = word_tokenize(row_words)

		for word in tokenized_words:
			# Lemmatize & fold case words
			word = lemmatizer.lemmatize(word)
			word = word.lower()
			
			if word in STOP_WORDS:
				continue

			INVERTED_INDEX[word].append(i)
		i+=1 

	csvDataFile.close()