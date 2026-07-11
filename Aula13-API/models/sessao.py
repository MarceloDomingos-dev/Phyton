from . import db
from .base import ModeloBase


class Sessao(ModeloBase):
    __tablename__ = "sessoes"

    filme_id = db.Column(db.Integer, db.ForeignKey("filmes.id"), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey("salas.id"), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    filme = db.relationship("Filme", back_populates="sessoes")
    sala = db.relationship("Sala", back_populates="sessoes")
    ingressos = db.relationship(
        "Ingresso",
        back_populates="sessao",
        cascade="all, delete-orphan",
    )

    @classmethod
    def listar_com_detalhes(cls):
        return cls.query.order_by(cls.data_hora.desc()).all()

    def __repr__(self):
        return f"<Sessao filme={self.filme_id} sala={self.sala_id}>"
