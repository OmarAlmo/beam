import csv
import pandas as pd
import  pre_process
import  collections
dictionary=pre_process.build_dictionary()
inverted_dictionary= pre_process.build_inverted_index()
vector_dictionary=collections.defaultdict(list)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import math
lemmatizer = WordNetLemmatizer()

CUSTOM_STOP_WORDS = ['course', 'knowledge', 'business', 'effectively','student','constitutes','introduce','major','minor', '(', ')', ',', '"','.', ';']
NLTK_WORDS = stopwords.words('english')
STOP_WORDS = CUSTOM_STOP_WORDS + NLTK_WORDS

'''create the keyword associated to the position of the elements within the document vectors '''
def generate_query(query):
        queryList=[]

        # Tokenize words
        tokenized_words = word_tokenize(query)

        for word in tokenized_words:
                # Lemmatize & fold case words
                word = lemmatizer.lemmatize(word)
                word = word.lower()
                
                if word in STOP_WORDS:
                        continue
                if word in queryList:
                        continue
                queryList.append(word)
        return queryList

# initialize vector matrix with term frequence as default value
def make_Vectormatrix(queryList):
        #Initialise vector with 0's
        totalNum_document = len(dictionary)
        for query_element in queryList:
                vector_dictionary[query_element]=[0] * totalNum_document
        for word in inverted_dictionary:
                if word in vector_dictionary:
                        for x in inverted_dictionary[word]:
                                vector_dictionary[word][x[0]-1]=x[1]
                else:
                        continue

        #make the dictionary to be tf-idf
        for term in vector_dictionary:
                print("(totalNum_document+1) ",(totalNum_document+1))
                print("inverted_dictionary[term] ",inverted_dictionary[term])
                print("len(inverted_dictionary[term]) ",len(inverted_dictionary[term]))
                if(len(inverted_dictionary[term])==0):
                        idf=0
                else:
                        idf=math.log((totalNum_document+1)/len(inverted_dictionary[term]))
                        print("idf for term ",term," is ",idf)
                for i in range(0,len(vector_dictionary[term])):
                        vector_dictionary[term][i]=vector_dictionary[term][i]*idf
        return vector_dictionary
def make_scoreTable(vector_dictionary):
        scoreTable=collections.defaultdict(list)
        #docID=0
        for i in range(0,len(dictionary)):
                score=0
                for x in vector_dictionary:
                        #print("vector dic is ",vector_dictionary)
                        #print('x is '+x)
                        #print("i-1 is ",vector_dictionary[x][i-1])
                        score+=vector_dictionary[x][i-1]
                scoreTable[i]=score
        #remove the document with score 0
        zero_score=[]
        for doc in scoreTable:
                if scoreTable[doc]==0:
                        zero_score.append(doc)
        for x in zero_score:
                scoreTable.pop(x)
        return sorted(scoreTable.items(), key=lambda x: x[1],reverse=True) 

def make_idList(scoreTable):
        idList=[]
        for x in scoreTable:
                idList.append(x[0])
        return idList

def retrieve_documents(id_list):
        csvdictionary = open('dictionary.csv', 'r')
        dic = csv.reader(csvdictionary)
        save_dic=[]
        for row in dic:
                save_dic.append(row)
        output = []
        for id in id_list:
                output.append(save_dic[id])

        return output

        
def main(query):
        queryList=generate_query(query)
        matrix=make_Vectormatrix(queryList)
        scoreTable=make_scoreTable(matrix)
        idList=make_idList(scoreTable)
        documents = retrieve_documents(idList)
        return documents