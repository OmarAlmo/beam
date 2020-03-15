from flask import Flask,render_template, request

import models.boolean
import models.vsm_retrieval
from  middleware.utils import retrieve_documents


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def handle_data():
    query = request.form['query']
    model = request.form['model']

    
    try:
        bool_retrieval.LEMMATIZE = request.form.getlist("lemmatization")[0]
    except:
        pass
    
    try:
        bool_retrieval.NORMALIZE = request.form.getlist("normalization")[0]
    except:
        pass

    if model == 'corpus_acess':
        query_list = query.split(',')
        return render_template('index.html',res=retrieve_documents(query_list), query=query)
    
    elif model == 'boolean':
        res=bool_retrieval.main(query)

        # Reset settings for next query
        bool_retrieval.LEMMATIZE = True
        bool_retrieval.NORMALIZE = True
        return render_template('index.html',res=res, query=query)
    
    else: 
        return render_template('index.html',res=vsm_retrieval.main(query), query=query)


if __name__ =="__main__":
    print("App initiated.")
    app.run(port=8080)





			