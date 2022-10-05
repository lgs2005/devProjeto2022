from datetime import datetime

from flask_jwt_extended import current_user
from init import db

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped


def extrair_campos(*campos):
	return lambda self: { campo: self.__getattribute__(campo) for campo in campos }


class Usuario(db.Model):
	__tablename__ = 'usuario'

	id: Mapped[int] = Column(Integer, primary_key=True)

	nome: Mapped[str] = Column(String(255), nullable=False)
	email: Mapped[str] = Column(String(255), nullable=False, unique=True)
	pwhash: Mapped[str] = Column(String(60), nullable=False)

	dados = extrair_campos('id', 'nome', 'email')
	logado: 'Usuario' = current_user


class Pasta(db.Model):
	__tablename__ = 'pasta'

	id: Mapped[int] = Column(Integer, primary_key=True)
	nome: Mapped[str] = Column(String(255), nullable=False)

	paginas: Mapped['list[Pagina]'] = db.relationship('Pagina', back_populates='pasta')


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

	dados = extrair_campos('id', 'id_autor', 'nome', 'favorito', 'data_criacao', 'data_excluir')

	def tem_acesso(self, usuario: 'Usuario') -> bool:
		if self.id_autor == usuario.id:
			return True

		acesso = Acesso.query\
			.filter_by(
				id_usuario = usuario.id,
				id_pagina = self.id,
			)\
			.first()
			
		return acesso != None


class Acesso(db.Model):
	__tablename__ = 'acesso'

	usuario_id: Mapped[int] = Column(ForeignKey(Usuario.id), primary_key=True)
	pagina_id: Mapped[int] = Column(ForeignKey(Pagina.id), primary_key=True)

	usuario: Mapped[Usuario] = db.relationship(Usuario)
	pagina: Mapped[Pagina] = db.relationship(Pagina)

	data_expira = Column(DateTime, nullable=True)
