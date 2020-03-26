from flask import Flask, render_template, request

import models.boolean
import models.vsm
from middleware.utils import retrieve_documents

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def handle_data():
    query = request.form['query']
    model = request.form['model']
    corpus = request.form['corpus']
    globalexpansion = request.form.get('globalexpansion')
    print(str(query))
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
        res = models.boolean.main(corpus,query, globalexpansion)

        # Reset settings for next query
        models.boolean.LEMMATIZE = True
        models.boolean.NORMALIZE = True
        return render_template('index.html',
                                flag=True, 
                                res=res, 
                                query=str(query),
                                corpus=corpus)

    else:
        res = models.vsm.main(corpus, query, globalexpansion)
        return render_template('index.html',
                               flag=True,
                               res=res,
                               query=str(query),
                               corpus=corpus)


if __name__ == "__main__":
    print("App initiated.")
    app.run(port=8080)
