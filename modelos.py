from datetime import datetime

from flask_login import UserMixin

from init import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    pwhash = db.Column(db.Text, nullable=False)

    def __str__(self) -> str:
        return f'<User {self.id}, {self.nome}, {self.email}, {self.pwhash}>'


class Pagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    caminho = db.Column(db.Text, nullable=False)
    favorito = db.Column(db.Boolean, nullable=False, default=False)

    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey(Usuario.id),
        nullable=False
    )
    usuario = db.relationship(Usuario)

    data_criacao = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    excluir_em = db.Column(db.DateTime, nullable=True)

    def json(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "excluir_em": self.excluir_em,
            "data_criacao": self.data_criacao,
            "favorito": self.favorito
        }

    def __str__(self):
        return f'<Pagina {self.id}, {self.id_usuario}, {self.nome}, {self.excluir_em}, {self.data_criacao}, {self.favorito}>'


class Compartilhamento(db.Model):
    id_usuario = db.Column(
        db.Integer,
        db.ForeignKey(Usuario.id),
        primary_key=True
    )

    id_pagina = db.Column(
        db.Integer,
        db.ForeignKey(Pagina.id),
        primary_key=True
    )
    
    usuario = db.relationship(Usuario)
    pagina = db.relationship(Pagina)

    def __str__(self):
        return f'<Compartilhamento {self.id_usuario}, {self.id_pagina}>'


# if __name__ == '__main__':
#     p = Pagina(id_usuario=1, nome='teste', conteudo='',
#                data_exclusao=0, data_criacao=0, favorito=False)

#     db.session.add(p)
#     db.session.commit()

# Selecione os comentários e digite: Ctrl + ;:
