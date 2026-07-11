from . import db
from .base import ModeloBase


class Sala(ModeloBase):
    __tablename__ = "salas"

    numero = db.Column(db.Integer, nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)

    sessoes = db.relationship("Sessao", back_populates="sala")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.numero).all()

    def __repr__(self):
        return f"<Sala {self.numero}>"
