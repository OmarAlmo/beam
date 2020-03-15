print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
import sys
from pathlib import Path

# if __name__ == '__main__' and __package__ is None:
# 	file = Path(__file__).resolve()
# 	parent, top = file.parent, file.parents[1]
# 	sys.path.append(str(top))
# 	try:
# 		sys.path.remove(str(parent))
# 	except ValueError: # Already removed
# 		pass
# 	print(sys.path)
# 	import beam.middleware
# 	__package__ = '.beam.middleware'

import csv
import pandas as pd
import re
import math

INDEX_REGEX = r'\[\d+, [+-]?[0-9]*[.]?[0-9]+\]'
NUMBER_DOCUMENTS = pd.read_csv("dictionary.csv").shape[0] - 1


def retrieve_documents(id_list):
	dictionary = open('dictionary.csv', 'r')
	dic = csv.reader(dictionary)

	ids = list(map(int, id_list))

	output = []

	df = pd.read_csv('dictionary.csv')
	df = df.set_index('DocID')

	for i in id_list:
		tmp =[df.iat[int(i),0], df.iat[int(i), 1]]
		output.append(tmp)
	return output

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

def get_term_docIDSeq(term):
	df = pd.read_csv("tfidf_index.csv", header=0)
	for i in range(0, df.shape[0]-1):
		if term == df.iloc[i]['Term']:
			row = df.iat[i,2]
			p = re.compile(INDEX_REGEX)
			index_list = p.findall(row)
			return [i[1 : -1].split(', ') for i in index_list]

def convert_to_list(line):
	p = re.compile(INDEX_REGEX)
	return [i[1 : -1].split(', ') for i in p.findall(line)]

def get_tf(term, docID):
	doc = get_document(docID)
	row = get_term_docIDSeq(term)
	try:
		for i in row:
			if (int(i[0]) == docID):
				return float(i[1])/float(len(doc))	
	except:
		return 0

def get_df(term):
	return len(get_term_docIDSeq(term))

def get_idf(term):
    return math.log10(NUMBER_DOCUMENTS/(get_df(term)+1))

def calculate_tfidf(term, docID):
	return get_tf(term, docID) * get_idf(term)

def get_tfidf(term, doc):
	df = pd.read_csv('inverted_index.csv')
	return df.loc[df['Term'] == term]['tfidf'].values
