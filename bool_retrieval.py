from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from stack import Stack
import csv
import pandas as pd
import re
import numpy


OPERATORS = ['AND', 'OR', 'AND_NOT', '(', ')']
PRECIDENT = {'(': 1, 'AND': 2, 'OR': 2, 'NOT': 2, 'AND_NOT': 2, }
PUNCUATIONS = [',', '[', ']', '']
INDEX_REGEX = r'(\[\d+, \d+\])'
lemmatizer = WordNetLemmatizer()

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
		listA = get_docs_ids(a)
	else:
		listA = a
	if type(b) != list:
		listB = get_docs_ids(b)
	else:
		listB = b

	if op == 'AND':
		res = list(set(listA).intersection(listB))
	elif op == 'OR':
		res = list(set(listA) | set(listB))
	else:  # op == 'AND_NOT':
		res = list(set(listA) not in set(listB))

	return res

def get_docs_ids(word):
	wildcard = False
	
	if '*' in word:
		wildcard = True

	index_file = open('inverted_index.csv', 'r')
	index = csv.reader(index_file)

	df = pd.read_csv("index.csv", header=0)
	word = lemmatizer.lemmatize(word.lower())
	output = []

	if wildcard:
		regx = re.compile(wildcard_to_regex(word))
		query = "re.match(regx, df.iloc[i]['Term'])"
	else:
		query = "(word == df.iloc[i]['Term'])"

	for i in range(0, df.shape[0]):
		if (eval(query)):
			row = df.iat[i,0]

			print(df.iat[i,0], "\n", df.iat[i,1], "\n\n")

			p = re.compile(INDEX_REGEX)
			index_list = p.findall(row)
			res = [i[1 : -1].split(', ') for i in index_list] 

			j = 0
			for j in range(len(res)):
				output.append(res[j][0])
				j+=1

	index_file.close()
	return(output)

def wildcard_to_regex(wildcard_word):
	w = list(wildcard_word)
	out = ""
	for c in w:
		if c == '*':
			c = '(.'+c+')'
		out += c
	return out

print(get_docs_ids('op*'))

def retrieve_documents(id_list):
	dictionary = open('dictionary.csv', 'r')
	dic = csv.reader(dictionary)

	output = []

	i = 1
	for row in dic:
		if row == []:
			continue
		if str(i) in id_list:
			output.append(row)
		i+=1
	return output


def main(query):
	if len(query.split()) < 2:
		ids = get_docs_ids(query)
		documents = retrieve_documents(ids)
	else:
		postfixquery = infixToPostfix(query)
		ids = processPostfix(postfixquery)
		documents = retrieve_documents(ids)
	return documents
