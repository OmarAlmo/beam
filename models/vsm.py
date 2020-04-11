if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"

from middleware import utils 
from middleware import relevance

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import difflib
import  collections

lemmatizer = WordNetLemmatizer()

CUSTOM_STOP_WORDS = ['course', 'knowledge', 'business', 'effectively','student','constitutes','introduce','major','minor', '(', ')', ',', '"','.', ';']
NLTK_WORDS = stopwords.words('english')
STOP_WORDS = CUSTOM_STOP_WORDS + NLTK_WORDS

def process_query(corpus, query, globalexpansion):
    '''
    input: query, corpus, bool if user wants global query expansion
    output: tokenized list of query with removed stop words and lemmatized & lower case words
    global query expansion done on words with df < 10
    '''
    output = set()
    query_list = word_tokenize(query)

    if (len(query_list) < 2): n = 5
    else: n = 2

    for word in query_list:
        if word in STOP_WORDS:
            continue
        else:
            if globalexpansion:
                synonyms = utils.get_synonym(word)
                print("synonym for ", word)
                try: 
                    output.add(synonyms[0]) 
                    print("1st synonym: ",synonyms[0])
                except: pass

                try: 
                    output.add(synonyms[1])
                    print("2nd synonym: ", synonyms[1])
                except: pass
            
            output.add(lemmatizer.lemmatize(word.lower()))
    return list(output)

def measure_scores(corpus,query, topic):
    '''
    retreive docIDs and tfidf then if reuters remove unwanted docs by topic selected
    '''
    scores = collections.defaultdict(list)
    for term in query:
        row = utils.get_term_docIDSeq(corpus,term)
        for i in row:
            docID = i[0]
            tfidf = i[1]
            if docID in scores.keys():
                scores[docID] += float(tfidf)
            else:
                scores[docID] = float(tfidf)
    if corpus == 'reuters':
        return utils.filter_documents_topic(scores, topic, 'vsm')
    else:
        return scores

def rerank_scores_return_id(scores, relevantRanked):
    if len(relevantRanked.items()) != 0:
        for k, v in relevantRanked.items():
            scores[k] = v

    sorted_ranking = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
    ids = []
    for k, v in sorted_ranking.items():
        ids.append(k)
    return ids

def main(corpus,query,globalexpansion, topic):
    query_list = process_query(corpus,query, globalexpansion)
    measureScores = measure_scores(corpus,query_list, topic)
    newRanking = relevance.local_expansion(corpus, query, measureScores)
    ids_ranking = rerank_scores_return_id(measureScores, newRanking)
    print("Retreiving documents.")
    return utils.retrieve_documents(corpus,ids_ranking[:15])
