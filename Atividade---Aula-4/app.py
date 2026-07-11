from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profissional')
def profissional():
    return render_template('profissional.html')

@app.route('/expectativas')
def expectativas():
    return render_template('expectativas.html')

if __name__ == '__main__':
    app.run(debug=True)
