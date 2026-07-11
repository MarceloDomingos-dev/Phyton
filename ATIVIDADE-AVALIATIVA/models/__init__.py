from flask_sqlalchemy import SQLAlchemy

# db é usado por todos os Models para criar tabelas e colunas.
db = SQLAlchemy()

from .base import ModeloBase
from .filme import Filme
from .sala import Sala
from .sessao import Sessao
from .ingresso import Ingresso

__all__ = ["db", "ModeloBase", "Filme", "Sala", "Sessao", "Ingresso"]
