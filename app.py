from flask import Flask, render_template, request

import models.boolean
import models.vsm
from middleware.utils import retrieve_documents, RELEVANT_DOCS, NRELEVANT_DOCS

app = Flask(__name__)

# RELEVANT_DOCS = collections.defaultdict(list)
# NRELEVANT_DOCS = collections.defaultdict(list)

@app.route('/')
def index():
    return render_template('index.html')

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

    if model == 'corpus_acess':
        query_list = query.split(',')
        return render_template('index.html',
                               res=retrieve_documents(corpus, query_list),
                               query=query,
                               corpus=corpus)

    elif model == 'boolean':
        res = models.boolean.main(corpus,query, globalexpansion, topic)

        # Reset settings for next query
        models.boolean.LEMMATIZE = True
        models.boolean.NORMALIZE = True
        return render_template('index.html',
                                flag=True,
                                res=res, 
                                model=model,
                                query=query,
                                corpus=corpus)

    else:
        res = models.vsm.main(corpus, query, globalexpansion, topic)
        return render_template('index.html',
                               flag=True,
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


if __name__ == "__main__":
    print("App initiated.")
    app.run(port=8080,debug=True)
