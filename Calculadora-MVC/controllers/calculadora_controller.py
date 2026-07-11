from flask import Blueprint, render_template, request

from models import Operacao

calculadora_bp = Blueprint("calculadora", __name__)


@calculadora_bp.route("/", methods=["GET", "POST"])
def index():
    resultados = None
    etapas = None

    if request.method == "POST":
        try:
            num1 = float(request.form.get("num1"))
            operador = request.form.get("operacao")

            if operador == "sqrt":
                num2 = None
            else:
                num2 = float(request.form.get("num2"))

            operacao = Operacao.criar_e_salvar(num1, operador, num2)
            resultados = operacao.resultado
            etapas = operacao.etapas

        except ValueError as erro:
            etapas = str(erro)
            resultados = "Erro"

    historico = Operacao.query.order_by(Operacao.criado_em.desc()).all()

    return render_template(
        "calculadora.html",
        etapas=etapas,
        resultados=resultados,
        historico=historico,
    )
