# Cenário: B - Cinema
# Aluno: Marcelo Domingos

import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for

from controllers import api_v1_bp, cinema_bp
from models import Filme, Sala, db

load_dotenv()


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "ATIVIDADE_AVALIATIVA.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(cinema_bp)
    app.register_blueprint(api_v1_bp)

    @app.route("/")
    def index():
        return redirect(url_for("cinema.index"))

    with app.app_context():
        db.create_all()
        popular_dados_iniciais()

    return app


def popular_dados_iniciais():
    """Cria filmes e salas iniciais para o formulário já funcionar."""
    if Filme.query.count() == 0:
        db.session.add_all(
            [
                Filme(titulo="O Auto da Compadecida", duracao_min=104, classificacao="12"),
                Filme(titulo="Central do Brasil", duracao_min=110, classificacao="L"),
                Filme(titulo="Divertida Mente 2", duracao_min=96, classificacao="L"),
            ]
        )

    if Sala.query.count() == 0:
        db.session.add_all(
            [
                Sala(numero=1, capacidade=80),
                Sala(numero=2, capacidade=120),
                Sala(numero=3, capacidade=60),
            ]
        )

    db.session.commit()


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
