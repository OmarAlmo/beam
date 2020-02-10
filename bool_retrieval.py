from nltk.tokenize import word_tokenize
import re
from pythonds.basic.stack import Stack
import csv
import pandas as pd

OPERATORS = ['AND', 'OR', 'AND_NOT', '(', ')']
PRECIDENT = {'(': 1, 'AND': 2, 'OR': 2, 'NOT': 2, 'AND_NOT': 2,}

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
	print(postfix_list)
	for word in postfix_list:
		if word not in OPERATORS:
			stack.push(word)
		else:
			a = stack.pop()
			b = stack.pop()
			op = word
			res = boolean_retrieval(a, b, op)
			print("RES: ", res)
			stack.push(res)

	output = []
	while (not stack.isEmpty()):
		output.append(stack.pop())

	print(output)
	return output


def boolean_retrieval(a, b ,op):

	if type(a) != list:
		listA = getDocIds(a)
		print("LIST A: ",listA)
	else: listA = a
	if type(b) != list:
		listB = getDocIds(b)
		print("LIST B: ",listB)
	else: listB = b
	
	if op == 'AND':
		res = list(set(listA).intersection(listB))
	elif op == 'OR':
		res = list(set(listA) | set(listB))
	else: #op == 'AND_NOT':
		res = list(set(listA) not in set(listB))
	
	return res

def getDocIds(word):
	index_file = open('index.csv', 'r')
	index = csv.reader(index_file)

	for row in index:
		if word == row[0]:
			return row[1]
	return []
	
	index_file.close()

def retrieve_documents(id_list):
	dictionary = open('dictionary.csv', 'r')
	dic = csv.reader(dictionary)

	output = []

	df = pd.read_csv("dictionary.csv", header=0)
	for i in id_list:
		output.append(df.iloc[i])
	
	return output


def main(query):
	postfixquery = infixToPostfix(query)
	print(postfixquery)
	ids = processPostfix(postfixquery)
	
	# output = retrieve_documents(ids)
	# print(output)


booleanquery = "ADM AND (CSI OR system)"
main(booleanquery)



			