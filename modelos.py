from datetime import datetime, timezone
from typing import Callable

from flask_jwt_extended import get_current_user
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        select)
from sqlalchemy.orm import Mapped

from init import db


def extrair_campos(*campos):
    return lambda self: {campo: self.__getattribute__(campo) for campo in campos}


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id: Mapped[int] = Column(Integer, primary_key=True)

    nome: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True)
    hash_senha: Mapped[str] = Column(String(60), nullable=False)

    dados = extrair_campos('id', 'nome', 'email')
    atual: 'Callable[[], Usuario]' = lambda: get_current_user()


class Pagina(db.Model):
    __tablename__ = 'pagina'
    id: Mapped[int] = Column(Integer, primary_key=True)

    id_autor = Column(ForeignKey(Usuario.id))
    autor = db.relationship(Usuario)

    nome = Column(String(255), nullable=False)
    arquivo = Column(String(32), nullable=False)

    favorito = Column(Boolean, nullable=False, default=False)

    data_excluir = Column(DateTime, nullable=True)
    data_criacao = Column(DateTime, nullable=False,
                          default=datetime.now(timezone.utc))

    dados = extrair_campos('id', 'id_autor', 'nome',
                           'favorito', 'data_excluir', 'data_criacao')

    def permite_acesso(self, usuario: Usuario) -> bool:
        if usuario.id == self.id_autor:
            return True
        else:
            acesso = db.session.execute(
                select(Acesso).filter(
                    Acesso.id_usuario == self.id_autor,
                    Acesso.id_pagina == self.id,
                )
            ).first()

            return acesso != None


class Acesso(db.Model):
    __tablename__ = 'acesso'

    id_usuario = Column(ForeignKey(Usuario.id), primary_key=True)
    id_pagina = Column(ForeignKey(Pagina.id), primary_key=True)

    usuario = db.relationship(Usuario)
    pagina = db.relationship(Pagina)

    data_expira = Column(DateTime, nullable=True)
