from . import db
from .base import ModeloBase


class Ingresso(ModeloBase):
    """Tabela opcional do cenário Cinema."""

    __tablename__ = "ingressos"

    sessao_id = db.Column(db.Integer, db.ForeignKey("sessoes.id"), nullable=False)
    assento = db.Column(db.String(10), nullable=False)
    nome_comprador = db.Column(db.String(120), nullable=False)

    sessao = db.relationship("Sessao", back_populates="ingressos")
