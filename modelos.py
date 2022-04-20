from sqlalchemy import ForeignKey
from init import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    pwhash = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f'<User {self.id}, {self.nome}, {self.email}, {self.pwhash}>'

class Pagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id))
    nome = db.Column(db.Text, nullable=False)
    conteudo = db.Column(db.Text, nullable=False) # armazenar link para arquivo JSON 
    data_exclusao = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.Integer, nullable=False)
    favorito = db.Column(db.Boolean, nullable=False)

class Compartilhamento(db.Model):
    id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id))
    id_pagina = db.Column(db.Integer, db.ForeignKey(Pagina.id))