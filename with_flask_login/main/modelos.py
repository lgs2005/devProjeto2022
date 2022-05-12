from config import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin): # UserMixin necessário para obter funções do 'flask_login' 
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    pwhash = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f'<User {self.id}, {self.nome}, {self.email}, {self.pwhash}>'


class Pagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id), nullable=False)
    usuario = db.relationship('Usuario')

    nome = db.Column(db.Text, nullable=False)
    conteudo = db.Column(db.Text, nullable=False) # TODO: armazenar link para arquivo JSON 
    data_criacao = db.Column(db.Date, nullable=False) # DEFAULT: date.today()
    data_exclusao = db.Column(db.Date) # TODO: DEFAULT: on_delete(date.today() + relativedelta(days=30)) ------ relativedelta: pacote dateutil
    is_favorito = db.Column(db.Boolean, nullable=False)

    def __str__(self) -> str:
        return f'<Pagina {self.id}, {self.id_usuario}, {self.nome}, {self.data_criacao}, {self.data_exclusao}, {self.is_favorito}>'

    def toJson(self) -> dict:
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "conteudo": self.conteudo,
            "data_exclusao": self.data_exclusao,
            "data_criacao": self.data_criacao,
            "favorito": self.is_favorito
        }


class Compartilhamento(db.Model):
    id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id), primary_key=True)
    id_pagina = db.Column(db.Integer, db.ForeignKey(Pagina.id), primary_key=True)
    usuario = db.relationship('Usuario')
    pagina = db.relationship('Pagina')

    def __str__(self) -> str:
        return f'<Compartilhamento {self.id_usuario}, {self.id_pagina}>'