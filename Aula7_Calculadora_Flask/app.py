from flask import Flask, render_template
from calculadora import calcular

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return calcular()

if __name__ == '__main__':
    app.run(debug=True)
