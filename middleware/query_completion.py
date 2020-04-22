if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "middleware"


import middleware.utils as utils


def get_max_frequence(dict):
    maxNum=0
    for x in dict.values():
        if(x==None):
            return 0
        if maxNum<int(x[1]):
            maxNum=int(x[1])
    return maxNum

def active_query_completion(corpus,word):
    Resultlist=[]
    todelete=None
    bigramDict=utils.get_bigramDict_by_word(corpus,word)
    # print(bigramDict)
    for i in range(0,5):
        
        maxNum=get_max_frequence(bigramDict)
        print(maxNum)
        if maxNum==0:
            break
        for x,y in bigramDict.items():
            if(int(y[1])==maxNum):
                todelete=x
                Resultlist.append(y[0])
                break
        bigramDict.pop(todelete)
    return Resultlist

    

# print("active_query_completion('reuters', 'canada')")
# print(active_query_completion('reuters', 'canada'))

# print("active_query_completion('reuters', 'bank')")
# print(active_query_completion('reuters', 'bank'))

# print("active_query_completion('reuters', 'coffee')")
# print(active_query_completion('reuters', 'coffee'))

# print("active_query_completion('reuters', 'stock')")
# print(active_query_completion('reuters', 'stock'))

# print("active_query_completion('reuters', 'oil')")
print(active_query_completion('reuters', 'oil'))
