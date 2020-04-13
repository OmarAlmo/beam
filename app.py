from flask import Flask, render_template, request

import models.boolean
import models.vsm
from middleware.utils import retrieve_documents, RELEVANT_DOCS, NRELEVANT_DOCS
import middleware.query_completion as completion
import json

app = Flask(__name__)

TOPICS_LIST = ['all', 'lei', 'earn', 'acq', 'interest', 'trade', 'crude', 'carcass', 'gnp', 'veg-oil',
 'jobs', 'money-fx', 'grain', 'alum', 'bop', 'sugar', 'ship', 'heat', 'cotton',
 'gold', 'coffee', 'reserves', 'cpi', 'tin', 'cocoa', 'retail', 'money-supply',
 'pet-chem', 'nat-gas', 'iron-steel', 'housing', 'copper', 'jet', 'rubber',
 'orange', 'wpi', 'ipi', 'nickel', 'potato', 'instal-debt', 'gas', 'fuel',
 'oilseed', 'zinc', 'rand', 'lumber', 'silver', 'lead', 'livestock',
 'strategic-metal', 'yen', 'income', 'meal-feed', 'tea', 'platinum', 'propane']

@app.route('/')
def index():
    return render_template('index.html', topics=TOPICS_LIST)

@app.route('/', methods=['POST'])
def handle_data():
    query = request.form['query']
    model = request.form['model']
    corpus = request.form['corpus']
    globalexpansion = request.form.get('globalexpansion')

    if corpus == 'reuters': topic = request.form['topicDropdown']
    else: topic = 'All'

    try: models.boolean.LEMMATIZE = request.form.getlist("lemmatization")[0]
    except: pass
    try: models.boolean.NORMALIZE = request.form.getlist("normalization")[0]
    except: pass

    try: models.vsm.LEMMATIZE = request.form.getlist("lemmatization")[0]
    except: pass
    try: models.vsm.NORMALIZE = request.form.getlist("normalization")[0]
    except: pass

    noDoc=False

    if model == 'corpus_acess':
        query_list = query.split(',')
        return render_template('index.html',
                               topics=TOPICS_LIST,
                               res=retrieve_documents(corpus, query_list),
                               query=query,
                               corpus=corpus)

    elif model == 'boolean':
        res = models.boolean.main(corpus,query, globalexpansion, topic)
        if type(res) == str: noDoc=True
        # Reset settings for next query
        models.boolean.LEMMATIZE = True
        models.boolean.NORMALIZE = True
        return render_template('index.html',
                                flag=True,
                                topics=TOPICS_LIST,
                                noDoc=noDoc,
                                res=res, 
                                model=model,
                                query=query,
                                corpus=corpus)

    else:
        res = models.vsm.main(corpus, query, globalexpansion, topic)
        query=" ".join(models.vsm.process_query(corpus, query, globalexpansion))
        return render_template('index.html',
                               flag=True,
                               topics=TOPICS_LIST,
                               res=res,
                               model=model,
                               query=query,
                               corpus=corpus)

# Handle relevance
@app.route('/relevance', methods=['POST'])
def relevance():

    relevance = str(request.data).split(",")

    if (relevance[0] == "b'relevant"):
        docID = relevance[1]
        q = relevance[2].replace("'","")
        print("Q2", q)
        if q in RELEVANT_DOCS.keys():
            RELEVANT_DOCS[q] += [docID]
        else:
            RELEVANT_DOCS[q] = [docID]
    else:
        docID = relevance[1]
        q = relevance[2].replace("'","")
        if q in NRELEVANT_DOCS.keys():
            NRELEVANT_DOCS[q] += [docID]
        else:
            NRELEVANT_DOCS[q] = [docID]
    print("RELEVANT:", RELEVANT_DOCS)
    print("NRELEVANT:", NRELEVANT_DOCS)
    return ('')


@app.route('/')
def get_query_completion_output():
    globalexpansion = request.form.get('globalexpansion')
    corpus = request.form['corpus']
    query = request.form['query']
    tmpquery=query
    query="".join(models.vsm.process_query(corpus, query, globalexpansion))
    tmpquery=tmpquery.split(" ")[-1]
    result= completion.active_query_completion(corpus,tmpquery)
    return result


if __name__ == "__main__":
    print("App initiated.")
    app.run(port=8080,debug=True)
