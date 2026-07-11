from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Página inicial</h1>"


@app.route("/decorator")
def decorator():
    return """
    <h1>Decorator em Python</h1>

    <p>
    Decorators são funções utilizadas para modificar ou adicionar comportamentos
    a outras funções sem alterar diretamente seu código original.
    </p>

    <p>
    Eles servem para reutilizar lógica, organizar melhor o código e evitar repetição.
    </p>

    <p>
    No Flask, decorators são usados para definir rotas.
    Exemplo:
    </p>

    <pre>
    @app.route("/home")
    def home():
        return "Olá"
    </pre>

    <p>
    Nesse caso, o decorator @app.route informa ao Flask qual URL executará a função.
    </p>
    """


if __name__ == "__main__":
    app.run(debug=True)
