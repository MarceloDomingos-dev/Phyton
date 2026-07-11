from datetime import datetime
from math import sqrt

from . import db


class Operacao(db.Model):
    __tablename__ = "operacoes"

    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Float, nullable=False)
    num2 = db.Column(db.Float, nullable=True)
    operador = db.Column(db.String(10), nullable=False)
    resultado = db.Column(db.Float, nullable=False)
    etapas = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Operacao {self.id}: {self.etapas}>"

    @staticmethod
    def calcular(num1, operador, num2=None):
        if operador == "+":
            resultado = num1 + num2
            etapas = f"{num1} + {num2} = {resultado}"
        elif operador == "-":
            resultado = num1 - num2
            etapas = f"{num1} - {num2} = {resultado}"
        elif operador == "*":
            resultado = num1 * num2
            etapas = f"{num1} × {num2} = {resultado}"
        elif operador == "/":
            if num2 == 0:
                raise ValueError("Não é possível dividir por zero.")
            resultado = num1 / num2
            etapas = f"{num1} ÷ {num2} = {resultado}"
        elif operador == "**":
            resultado = num1 ** num2
            etapas = f"{num1} ^ {num2} = {resultado}"
        elif operador == "sqrt":
            if num1 < 0:
                raise ValueError("Não é possível calcular raiz quadrada de número negativo.")
            resultado = sqrt(num1)
            etapas = f"√{num1} = {resultado}"
        else:
            raise ValueError("Operação inválida.")

        return resultado, etapas

    @classmethod
    def criar_e_salvar(cls, num1, operador, num2=None):
        resultado, etapas = cls.calcular(num1, operador, num2)

        operacao = cls(
            num1=num1,
            num2=num2,
            operador=operador,
            resultado=resultado,
            etapas=etapas,
        )

        db.session.add(operacao)
        db.session.commit()

        return operacao
