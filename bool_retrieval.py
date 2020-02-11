from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
# from stack import Stack
from pythonds.basic.stack import Stack
import csv
import pandas as pd
import re

OPERATORS = ['AND', 'OR', 'AND_NOT', '(', ')']
PRECIDENT = {'(': 1, 'AND': 2, 'OR': 2, 'NOT': 2, 'AND_NOT': 2, }
PUNCUATIONS = [',', '[', ']', '']
INDEX_REGEX = r'(\[\d+, \d+\])'
lemmatizer = WordNetLemmatizer()

'''
INPUT = ADM AND (CSI OR system)
OUTPUT = ADM CSI system OR AND
'''


def infixToPostfix(query):
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
			while not stack.isEmpty() and PRECIDENT[stack.peek()] >= PRECIDENT[word]:
				postfix.append(stack.pop())
			stack.push(word)

	while not stack.isEmpty():
		postfix.append(stack.pop())
	return ' '.join(postfix)


def processPostfix(postfix):
	postfix_list = word_tokenize(postfix)
	stack = Stack()
	tmp = []
	for word in postfix_list:
		if word not in OPERATORS:
			stack.push(word)
		else:
			a = stack.pop()
			b = stack.pop()
			op = word
			res = boolean_retrieval(a, b, op)
			tmp.append(res)
			stack.push(res)

	output = []
	for i in tmp[0]:
		elem = str(i).strip()
		if elem not in PUNCUATIONS:
			output.append(elem)
	return output


def boolean_retrieval(a, b, op):
	if type(a) != list:
		listA = getDocIds(a)
		# print("LIST A: ", listA)
	else:
		listA = a
	if type(b) != list:
		listB = getDocIds(b)
		# print("LIST B: ", listB)
	else:
		listB = b

	if op == 'AND':
		res = list(set(listA).intersection(listB))
	elif op == 'OR':
		res = list(set(listA) | set(listB))
	else:  # op == 'AND_NOT':
		res = list(set(listA) not in set(listB))

	return res


def getDocIds(word):
	index_file = open('index.csv', 'r')
	index = csv.reader(index_file)

	df = pd.read_csv("index.csv", header=0)
	word = lemmatizer.lemmatize(word.lower())
	output = []

	for i in range(0, df.shape[0]):
		if (word == df.iloc[i]['Term']):
			row = df.iat[i,1]

			p = re.compile(INDEX_REGEX)
			index_list = p.findall(row)
			res = [i[1 : -1].split(', ') for i in index_list] 

			i = 0
			for i in range(len(res)):
				output.append(res[i][0])
				i+=1

			index_file.close()

			return(output)
	return []


def retrieve_documents(id_list):
	print(id_list)
	dictionary = open('dictionary.csv', 'r')
	dic = csv.reader(dictionary)

	output = []

	df = pd.read_csv("dictionary.csv", header=0)
	i=0
	for i in range(0, len(id_list)):
		output.append(df.iloc[[i]])
	return output

def main(query):
	postfixquery = infixToPostfix(query)
	print("postfixquery::",postfixquery)
	ids = processPostfix(postfixquery)
	print("ids::",ids)
	documents = retrieve_documents(ids)
	print("*****************************************")
	print("documents::",documents)

