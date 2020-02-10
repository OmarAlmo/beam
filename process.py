import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import collections

import csv

df = pd.read_csv("./corpus/parsed_UofO_Courses.csv")
lemmatizer = WordNetLemmatizer()

NUMBER_OF_ROWS = df.shape[0]

CUSTOM_STOP_WORDS = ['course', 'knowledge', 'business', 'effectively','student','constitutes','introduce','major','minor', '(', ')', ',', '"','.', ';']
NLTK_WORDS = stopwords.words('english')
STOP_WORDS = CUSTOM_STOP_WORDS + NLTK_WORDS

DICTIONARY = open('dictionary.csv', 'w')

INVERTED_INDEX = collections.defaultdict(list)
	
def build_dictionary():
	dictionary_writer = csv.writer(DICTIONARY)
	dictionary_writer.writerow(['docID', 'document'])
	csvDataFile = open('./corpus/parsed_UofO_Courses.csv')
	csvReader = csv.reader(csvDataFile)

	i = 0
	for row in csvReader:
		title = row[0]
		description = row[1]
		title_desc = title + description
		# newNode = Node(title, description)
		# DICTIONARY[i] = newNode
		dictionary_writer.writerow([i,title_desc])
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


def export_to_csv(invertedMap):

	index_file = open('index_file.csv', 'w')
	index = csv.writer(index_file)
	index.writerow(['key', 'docID_list'])

	for k, v in invertedMap.items():
		index.writerow([k, v])

	index_file.close()

build_index()
export_to_csv(INVERTED_INDEX)