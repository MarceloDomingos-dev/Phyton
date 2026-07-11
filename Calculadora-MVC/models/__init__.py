from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .operacao import Operacao

__all__ = ["db", "Operacao"]
