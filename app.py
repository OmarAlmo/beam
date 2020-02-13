from flask import Flask,render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def handle_data():
    query = request.form['query']
    model = request.form['model']
    print(query)
    print(model)
    return render_template('index.html')
		

if __name__ =="__main__":
    app.run(debug=True,port=8080)

			