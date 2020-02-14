from flask import Flask,render_template, request
import bool_retrieval
import vsm_retrieval


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def handle_data():
    query = request.form['query']
    model = request.form['model']
    
    if model == 'boolean':
        return render_template('index.html',res=bool_retrieval.main(query), query=query)
    else: 
        return render_template('index.html',res=vsm_retrieval.main(query), query=query)
		

if __name__ =="__main__":
    app.run(debug=True,port=8080)




			