from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from models import Filme, Sala, Sessao, db

# Blueprint = módulo de rotas do cinema.
# No HTML, o url_for usa o apelido "cinema", por exemplo: cinema.index.
cinema_bp = Blueprint("cinema", __name__, url_prefix="/cinema")


@cinema_bp.route("/")
def index():
    sessoes = Sessao.listar_com_detalhes()
    return render_template("cinema/lista_sessoes.html", sessoes=sessoes)


@cinema_bp.route("/sessao/cadastrar", methods=["GET", "POST"])
def cadastrar_sessao():
    filmes = Filme.listar()
    salas = Sala.listar()

    if request.method == "POST":
        filme_id = request.form.get("filme_id", type=int)
        sala_id = request.form.get("sala_id", type=int)
        data_hora_texto = request.form.get("data_hora", "")
        preco = request.form.get("preco", type=float)

        if not filme_id or not sala_id or not data_hora_texto or preco is None:
            return render_template(
                "cinema/formulario_sessao.html",
                filmes=filmes,
                salas=salas,
                erro="Preencha todos os campos corretamente.",
            )

        try:
            data_hora = datetime.fromisoformat(data_hora_texto)
        except ValueError:
            return render_template(
                "cinema/formulario_sessao.html",
                filmes=filmes,
                salas=salas,
                erro="Data e hora inválidas.",
            )

        sessao = Sessao(
            filme_id=filme_id,
            sala_id=sala_id,
            data_hora=data_hora,
            preco=preco,
        )
        db.session.add(sessao)
        db.session.commit()
        return redirect(url_for("cinema.index"))

    return render_template(
        "cinema/formulario_sessao.html",
        filmes=filmes,
        salas=salas,
    )
