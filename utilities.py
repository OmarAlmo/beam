import csv
import pandas as pd
import re

INDEX_REGEX = r'(\[\d+, \d+\])'
INDX_P = re.compile(INDEX_REGEX)


NUMBER_DOCUMENTS = pd.read_csv("dictionary.csv", header=0).shape[0]


def retrieve_documents(id_list):
	dictionary = open('dictionary.csv', 'r')
	dic = csv.reader(dictionary)

	ids = list(map(int, id_list))

	output = []

	df = pd.read_csv('dictionary.csv')
	df = df.set_index('DocID')

	for i in id_list:
		tmp =[df.iat[i,0], df.iat[i, 1]]
		output.append(tmp)

	return output

retrieve_documents([1,2,5,10])

def get_document(id):
	df = pd.read_csv('dictionary.csv')
	df = df.set_index('DocID')

	title = df.iat[id, 0]
	desc = df.iat[id, 1]

	if type(title) != str:
		title = ""
	if type(desc) != str:
		desc = ""

	return title + desc

def get_term_row(word):
	df = pd.read_csv("inverted_index.csv", header=0)

	for i in range(0, df.shape[0]):
		if word == df.iloc[i]['Term']:
			row = df.iat[i,1]
			p = re.compile(INDEX_REGEX)
			index_list = p.findall(row)

			return [i[1 : -1].split(', ') for i in index_list]

def convert_to_list(line):
	p = re.compile(INDEX_REGEX)
	return [i[1 : -1].split(', ') for i in p.findall(line)]
