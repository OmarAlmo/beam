from bs4 import BeautifulSoup
import csv
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import collections


CUSTOM_STOP_WORDS = ['course', 'knowledge', 'business', 'effectively','student','constitutes','introduce','major','minor', '(', ')', ',', '"','.', ';']
NLTK_WORDS = stopwords.words('english') + stopwords.words('french')
STOP_WORDS = CUSTOM_STOP_WORDS + NLTK_WORDS
INVERTED_INDEX = collections.defaultdict(list)


def build_dictionary():
    with open ('./corpus/UofO_Courses.html') as html_file:
        soup = BeautifulSoup(html_file, 'html5lib')

    dictionary_file = open('dictionary.csv', 'w')
    dictionary = csv.writer(dictionary_file)
    dictionary.writerow(['Course Title', 'Course Description'])


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
            if ("è" in course_description) or ("é" in course_description):
	            continue
            

        csv_writer.writerow([course_title, course_description])
    csv_file.close()


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

def export_indeverted_csv():
	inverted_csv_file = open('inverted_index.csv', 'w')
	csv_writer = csv.writer(inverted_csv_file)
	csv_writer.writerow(['Term', 'DocID&Sequence'])
	for key in INVERTED_INDEX:
		csv_writer.writerow([key, INVERTED_INDEX[key]])
	inverted_csv_file.close()