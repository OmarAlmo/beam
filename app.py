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

    try:
        models.boolean.LEMMATIZE = request.form.getlist("lemmatization")[0]
    except:
        pass

    try:
        models.boolean.NORMALIZE = request.form.getlist("normalization")[0]
    except:
        pass

    if model == 'corpus_acess':
        query_list = query.split(',')
        return render_template('index.html',
                               res=retrieve_documents(corpus, query_list),
                               query=query,
                               corpus=corpus)

    elif model == 'boolean':
        res = models.boolean.main(corpus,query)

        # Reset settings for next query
        models.boolean.LEMMATIZE = True
        models.boolean.NORMALIZE = True
        return render_template('index.html', 
                                res=res, 
                                query=query,
                                corpus=corpus)

    else:
        res = models.vsm.main(corpus, query)
        return render_template('index.html',
                               res=res,
                               query=query,
                               corpus=corpus)


if __name__ == "__main__":
    print("App initiated.")
    app.run(port=8080)
