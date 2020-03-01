import csv

def retrieve_documents(id_list):
	dictionary = open('dictionary.csv', 'r')
	dic = csv.reader(dictionary)

	ids = list(map(int, id_list))

	output = []

	i = 1
	for row in dic:
		if row == []:
			continue
		if i in ids:
			output.append(row)
		i+=1
	return output