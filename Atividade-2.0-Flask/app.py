import os
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy  # feito

app = Flask(__name__)
pasta_aula = os.path.abspath(os.path.dirname(__file__))

# Configuração da URI do SQLite (loja.db na pasta atual)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta_aula, "loja.db")  # feito
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # feito


# --- MODEL: tabela produtos ---
class Produto(db.Model):
    __tablename__ = "produtos"  # feito

    id = db.Column(db.Integer, primary_key=True)  # feito
    nome = db.Column(db.String(120), nullable=False)  # feito
    categoria = db.Column(db.String(60), nullable=False)  # feito
    preco = db.Column(db.Float, nullable=False)  # feito
    estoque = db.Column(db.Integer, nullable=False, default=0)  # feito

    def __repr__(self):
        return f"<Produto {self.id} {self.nome}>"


# Criar tabelas no banco de dados automaticamente
with app.app_context():
    db.create_all()  # feito


def _ler_formulario():
    """Lê campos do POST — nomes devem bater com o HTML (name=)."""
    return {
        "nome": request.form.get("nome", "").strip(),
        "categoria": request.form.get("categoria", "").strip(),
        "preco": request.form.get("preco", "").strip(),
        "estoque": request.form.get("estoque", "").strip(),
    }


def _validar(dados):
    if not dados["nome"] or not dados["categoria"] or not dados["preco"]:
        return "Preencha nome, categoria e preço."
    try:
        preco = float(dados["preco"].replace(",", "."))
        estoque = int(dados["estoque"] or 0)
    except ValueError:
        return "Preço ou estoque inválido."
    if preco < 0 or estoque < 0:
        return "Preço e estoque não podem ser negativos."
    return None


# --- READ ---
@app.route("/")
def index():
    produtos = Produto.query.order_by(Produto.nome).all()  # feito
    return render_template("lista.html", produtos=produtos)


# --- CREATE ---
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        dados = _ler_formulario()
        erro = _validar(dados)
        if erro:
            return render_template(
                "formulario.html",
                titulo="Cadastrar produto",
                erro=erro,
                **dados,
            )
        produto = Produto(
            nome=dados["nome"],
            categoria=dados["categoria"],
            preco=float(dados["preco"].replace(",", ".")),
            estoque=int(dados["estoque"] or 0),
        )
        db.session.add(produto)  # feito
        db.session.commit()  # feito
        return redirect(url_for("index"))

    return render_template("formulario.html", titulo="Cadastrar produto")


# --- UPDATE ---
@app.route("/editar/<int:produto_id>", methods=["GET", "POST"])
def editar(produto_id):
    produto = db.session.get(Produto, produto_id)  # feito

    if not produto:
        return redirect(url_for("index"))

    if request.method == "POST":
        dados = _ler_formulario()
        erro = _validar(dados)
        if erro:
            return render_template(
                "formulario.html",
                titulo="Editar produto",
                erro=erro,
                produto_id=produto.id,
                **dados,
            )
        produto.nome = dados["nome"]
        produto.categoria = dados["categoria"]
        produto.preco = float(dados["preco"].replace(",", "."))
        produto.estoque = int(dados["estoque"] or 0)
        db.session.commit()  # feito
        return redirect(url_for("index"))

    return render_template(
        "formulario.html",
        titulo="Editar produto",
        nome=produto.nome,
        categoria=produto.categoria,
        preco=produto.preco,
        estoque=produto.estoque,
        produto_id=produto.id,
    )


# --- DELETE ---
@app.route("/excluir/<int:produto_id>", methods=["POST"])
def excluir(produto_id):
    produto = db.session.get(Produto, produto_id)  # feito
    if produto:
        db.session.delete(produto)  # feito
        db.session.commit()  # feito
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)