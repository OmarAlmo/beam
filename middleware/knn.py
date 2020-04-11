if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"

from dotenv import load_dotenv
import sys, os, glob

from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import csv

csv.field_size_limit(sys.maxsize)

loadEnv = load_dotenv('./.env')
reutersDir = os.getenv('reuters_dir')

df = pd.read_csv('./reuters_index.csv', index_col=0)


TRAINING_SET = []
TRAINING_TOPICS = []

def get_topics():
    for file in glob.glob(os.path.join(reutersDir, 'all-topics-strings.lc.txt')):
        f = open(file, 'r')
        data = f.readlines()
        f.close()

        topics = []
        for t in data:
            topics.append(t.strip())
        topicNames = set(topics)
        categorizedTopics = {
                name: index for index, name in enumerate(topicNames)}

        return categorizedTopics


def set_training_test_sets(categorizedTopics):
    for i in range(df.shape[0]):
        if df.iat[i,1] in categorizedTopics: 
            TRAINING_SET.append(df.iloc[[i]])


def vectorize_and_train(topicsSet):
    X_arr, y_arr = [], []
    for doc in TRAINING_SET:
        text = str(doc["title"].values[0]) + str(doc["body"].values[0])
        topic = doc["topics"].values[0]

        X_arr.append(text)
        y_arr.append(topicsSet[topic])

    vectorizer = TfidfVectorizer(stop_words='english')
    X_train = vectorizer.fit_transform(X_arr)
    y_train = np.fromiter(y_arr, int)

    # Train
    knn = KNeighborsClassifier(n_neighbors=5, metric="euclidean")
    knn.fit(X_train, y_train)


    # predict topic of testing
    for i in range(df.shape[0]):
        title = df.iat[i,0]
        body = df.iat[i,4]
        text = [title + body]

        textVector = vectorizer.transform(text)
        predict = knn.predict(textVector)
        
        for k, v in topicsSet.items():
            if predict == v:
                print(i, k)
                df.iat[i,1] = k
    df.to_csv('reuters_index.csv')



topicsSet = get_topics()
set_training_test_sets(topicsSet)
vectorize_and_train(topicsSet)