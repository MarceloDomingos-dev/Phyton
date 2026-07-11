from datetime import datetime

from flask import Blueprint, jsonify, request

from models import Filme, Sala, Sessao, db
from services import TmdbApi

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
tmdb = TmdbApi()


@api_v1_bp.route("/sessoes", methods=["GET"])
def api_listar_sessoes():
    sessoes = Sessao.listar_com_detalhes()
    return jsonify([
        {
            "id": s.id,
            "filme": s.filme.titulo,
            "sala": s.sala.numero,
            "data_hora": s.data_hora.isoformat(),
            "preco": s.preco,
        }
        for s in sessoes
    ])


@api_v1_bp.route("/sessoes/<int:sessao_id>", methods=["GET"])
def api_detalhe_sessao(sessao_id):
    sessao = db.session.get(Sessao, sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessão não encontrada"}), 404
    return jsonify({
        "id": sessao.id,
        "filme": {
            "id": sessao.filme.id,
            "titulo": sessao.filme.titulo,
            "duracao_min": sessao.filme.duracao_min,
            "classificacao": sessao.filme.classificacao,
        },
        "sala": {
            "id": sessao.sala.id,
            "numero": sessao.sala.numero,
            "capacidade": sessao.sala.capacidade,
        },
        "data_hora": sessao.data_hora.isoformat(),
        "preco": sessao.preco,
    })


@api_v1_bp.route("/sessoes", methods=["POST"])
def api_criar_sessao():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body"}), 400
    try:
        sessao = Sessao(
            filme_id=int(dados["filme_id"]),
            sala_id=int(dados["sala_id"]),
            data_hora=datetime.fromisoformat(dados["data_hora"]),
            preco=float(dados["preco"]),
        )
    except (KeyError, ValueError):
        return jsonify({"erro": "Campos inválidos"}), 400
    db.session.add(sessao)
    db.session.commit()
    return jsonify({"id": sessao.id, "mensagem": "Sessão criada"}), 201


@api_v1_bp.route("/filmes", methods=["GET"])
def api_listar_filmes():
    return jsonify([
        {"id": f.id, "titulo": f.titulo, "duracao_min": f.duracao_min, "classificacao": f.classificacao}
        for f in Filme.listar()
    ])


@api_v1_bp.route("/salas", methods=["GET"])
def api_listar_salas():
    return jsonify([
        {"id": s.id, "numero": s.numero, "capacidade": s.capacidade}
        for s in Sala.listar()
    ])


@api_v1_bp.route("/externo/filmes/buscar", methods=["GET"])
def api_buscar_tmdb():
    termo = request.args.get("q", "")
    # request.args.get le o parametro opcional ?q=... sem gerar erro se ele nao for enviado.
    filmes, demo = tmdb.buscar(termo)
    return jsonify({
        "termo": termo,
        "fonte": "TMDB (demo)" if demo else "TMDB",
        "resultados": filmes,
    })


@api_v1_bp.route("/externo/filmes/populares", methods=["GET"])
def api_populares_tmdb():
    filmes, demo = tmdb.populares()
    return jsonify({
        "fonte": "TMDB (demo)" if demo else "TMDB",
        "resultados": filmes,
    })
