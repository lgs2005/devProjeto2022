from datetime import datetime
from typing import Callable

from flask_jwt_extended import get_current_user
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String)
from sqlalchemy.orm import Mapped

from init import db


def extrair_campos(*campos):
    return lambda self: {campo: self.__getattribute__(campo) for campo in campos}


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id: Mapped[int] = Column(Integer, primary_key=True)

    nome: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), nullable=False, unique=True)
    pwhash: Mapped[str] = Column(String(60), nullable=False)

    dados = extrair_campos('id', 'nome', 'email')
    atual: 'Callable[[], Usuario]' = lambda: get_current_user()


class Pasta(db.Model):
    __tablename__ = 'pasta'

    id: Mapped[int] = Column(Integer, primary_key=True)
    nome: Mapped[str] = Column(String(255), nullable=False)

    paginas: Mapped['list[Pagina]'] = db.relationship(
        'Pagina', back_populates='pasta')


class Pagina(db.Model):
    __tablename__ = 'pagina'

    id: Mapped[int] = Column(Integer, primary_key=True)

    autor_id: Mapped[int] = Column(ForeignKey(Usuario.id), nullable=False)
    autor: Mapped[Usuario] = db.relationship(Usuario)

    pasta_id: Mapped[int] = Column(ForeignKey(Pasta.id), nullable=False)
    pasta: Mapped[Pasta] = db.relationship(Pasta, back_populates='paginas')

    nome: Mapped[str] = Column(String(255), nullable=False)
    arquivo: Mapped[str] = Column(String(32), nullable=False)

    data_criacao: Mapped[datetime] = Column(DateTime, nullable=False)
    data_excluir: Mapped[datetime] = Column(DateTime, nullable=True)

    dados = extrair_campos('id', 'autor_id', 'nome', 'data_excluir', 'data_criacao')

    def permite_acesso(self, usuario: Usuario) -> bool:
        if usuario.id == self.id_autor:
            return True
        else:
            acesso = Acesso.query.filter_by(
                usuario_id=usuario.id,
                pagina_id=self.id,
            )

            return acesso != None


class Acesso(db.Model):
    __tablename__ = 'acesso'

    usuario_id: Mapped[int] = Column(ForeignKey(Usuario.id), primary_key=True)
    pagina_id: Mapped[int] = Column(ForeignKey(Pagina.id), primary_key=True)

    usuario: Mapped[Usuario] = db.relationship(Usuario)
    pagina: Mapped[Pagina] = db.relationship(Pagina)

    data_expira = Column(DateTime, nullable=True)
