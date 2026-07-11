from . import db
from .base import ModeloBase


class Filme(ModeloBase):
    __tablename__ = "filmes"

    titulo = db.Column(db.String(150), nullable=False)
    duracao_min = db.Column(db.Integer, nullable=False)
    classificacao = db.Column(db.String(5), nullable=False)

    sessoes = db.relationship("Sessao", back_populates="filme")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.titulo).all()

    def __repr__(self):
        return f"<Filme {self.titulo}>"
