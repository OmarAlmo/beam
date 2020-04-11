if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"
import middleware.utils as utils

import numpy as np

BETA, GAMMA = 0.75, 0.001 

def local_expansion(corpus, query, scores): 
    '''
    Input: query, unranked query scores, relevant docs, nrevelent docs
    output: ranked documents with relevant
    step 1: calcualte query vector 

    '''
    if len(utils.RELEVANT_DOCS.items()) == 0 and len(utils.NRELEVANT_DOCS.items()) == 0:
        return {}

    # convert scores to list 
    rankedDocIDs = []
    i = 0
    sorted_ranking = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
    for k, v in sorted_ranking.items():
        if i == 50: break
        temp = [k,v]
        rankedDocIDs.append(temp)
        i+=1

    # Step 1: genearte matrix of query words and frequecy in each ranked doc
    # {docID:[0,1,0]} docID and query vector
    queryList = query.split()
    step1 = {}
    # print(rankedDocIDs)
    for dID in rankedDocIDs:
        step1[dID[0]] = []
        for word in queryList:
            try: 
                wordCount = utils.get_document_content(corpus,int(dID[0])).lower().count(word)
                if wordCount == 0: wordCount = 0.1
            except: 
                wordCount = 0.1
            step1[dID[0]].append(wordCount)

    # clean releven/nrelevent docs to query
    r, nr = {}, {}
    for word in query.split():
        for q in utils.RELEVANT_DOCS:
            if word in q:
                r[q]= utils.RELEVANT_DOCS[q]
        
        for q in utils.NRELEVANT_DOCS:
            if word in q:
                nr[q]= utils.NRELEVANT_DOCS[q]

    # step 2 calcualte rocchio
    step2 = {}
    unrankedDoc = []

    for k, v in step1.items():
        flag1, flag2 = True, True
        try:
            if k in list(r.values())[0]:
                step2[k] = list(np.array(v) * BETA )
                flag1 = False
        except: pass
        try:
            if k in list(nr.values())[0]:
                step2[k] = list(np.array(v) * GAMMA)
                flag2 = False
        except:pass
        if flag1 and flag2: unrankedDoc.append(k)

    # remove unranked documents from revelance evaluation
    for u in unrankedDoc:
        del step1[u]
    
    print("Calcualting new ranking scores with rocchio")
    scores = {}
    for word in queryList:
        idf = utils.get_idf(corpus, word)
        i = 0
        for docID, v in step1.items():
            if i >= len(queryList):
                i = 0
            scores[docID] = 0.0
            docTF = list(v)[i]
            rocchio = list(step2.get(docID))[i]
            s = idf  * rocchio
            if s < 0: s = 0
            scores[docID] += s
            i+=1
    newRanking = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
    print(newRanking)
    return newRanking
