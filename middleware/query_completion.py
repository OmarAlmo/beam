import csv
import pandas as pd
import re
import math
import ast
import nltk
from nltk.corpus import wordnet, brown
import collections
import middleware.utils as utils



if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"



def get_max_frequence(dict):
    maxNum=0
    for x in dict.values():
        if(x==None):
            return 0
        if maxNum<int(x[1]):
            maxNum=int(x[1])
    print("max is ")
    print(maxNum)
    return maxNum
def active_query_completion(corpus,word):
    Resultlist=[]
    todelete=None
    bigramDict=utils.get_bigramDict_by_word(corpus,word)
    for i in range(0,5):
        
        maxNum=get_max_frequence(bigramDict)
        if maxNum==0:
            break
        for x,y in bigramDict.items():
            if(int(y[1])==maxNum):
                todelete=x
                Resultlist.append(y[0])
                break
        bigramDict.pop(todelete)
    return Resultlist

    