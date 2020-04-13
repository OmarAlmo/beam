if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"

import pandas as pd
import numpy as np
from weighted_levenshtein import levenshtein as lev


def check_word(corpus, term):
    '''
    check's if the word exists in the dictionary, if so return same word. 
    else, checks weighted distance with word and dictionary word, if distance is <= 1 then return word
    if not, then the smallest weight is returned
    '''
    if corpus == 'uottawa':
        df = pd.read_csv('./uottawa_dictionary.csv', index_col=0)
    else:
        df = pd.read_csv('./reuters_dictionary.csv', index_col=0)
    
    res = {}

    insert_costs = np.ones(128, dtype=np.float64) 
    delete_costs = np.ones(128, dtype=np.float64)
    substitute_costs = np.ones((128, 128), dtype=np.float64) 

    for i in range(df.shape[0]):
        if term == df.iat[i,0]:
            return df.iat[i,0]
        else:
            if len(str(df.iat[i,0])) >= len(term):
                weight = lev(term, str(df.iat[i,0]), insert_costs, delete_costs, substitute_costs)
                res[df.iat[i,0]] = weight
    
    sortedWeights = {k: v for k, v in sorted(res.items(), key=lambda item: item[1])}
    
    return (next(iter(sortedWeights)))
