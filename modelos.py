from init import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    pwhash = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f'<User {self.id}, {self.nome}, {self.email}, {self.pwhash}>'

class Pagina(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id), nullable=False)
    usuario = db.relationship('Usuario')

    nome = db.Column(db.Text, nullable=False)
    conteudo = db.Column(db.Text, nullable=False) # armazenar link para arquivo JSON 
    data_exclusao = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.Integer, nullable=False)
    favorito = db.Column(db.Boolean, nullable=False)

    def __str__(self):
        return f'<Pagina {self.id}, {self.id_usuario}, {self.nome}, {self.data_exclusao}, {self.data_criacao}, {self.favorito}>'

    def json(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "data_exclusao": self.data_exclusao,
            "data_criacao": self.data_criacao,
            "favorito": self.favorito
        }

class Compartilhamento(db.Model):
    id_usuario = db.Column(db.Integer, db.ForeignKey(Usuario.id), primary_key=True)
    id_pagina = db.Column(db.Integer, db.ForeignKey(Pagina.id), primary_key=True)
    usuario = db.relationship('Usuario')
    pagina = db.relationship('Pagina')

    def __str__(self):
        return f'<Pagina {self.id_usuario}, {self.id_pagina}>'

if __name__ == "__main__":
    p = Pagina(id_usuario=1, nome="teste", conteudo="", data_exclusao=0, data_criacao=0, favorito=False)

    db.session.add(p)
    db.session.commit()