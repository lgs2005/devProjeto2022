from init import db

def extrair_campos(*campos):
	return lambda self: { campo: self.__getattribute__(campo) for campo in campos }


class Usuario(db.Model):
	__tablename__ = 'Usuario'
	id = db.Column(db.Integer, primary_key=True)

	nome = db.Column(db.Text, nullable=False)
	email = db.Column(db.Text, unique=True, nullable=False)
	pwhash = db.Column(db.Text, nullable=False)

	dados = extrair_campos('id', 'nome', 'email')


class Pagina(db.Model):
	__tablename__ = 'Pagina'
	id = db.Column(db.Integer, primary_key=True)

	id_autor = db.Column(db.Integer, db.ForeignKey('Usuario.id'))
	autor = db.relationship(Usuario)

	nome = db.Column(db.Text, nullable=False)
	arquivo = db.Column(db.Text, nullable=False)

	favorito = db.Column(db.Boolean, nullable=False, default=False)

	data_criacao = db.Column(db.DateTime, nullable=False)
	data_excluir = db.Column(db.DateTime, nullable=True)

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
	__tablename__ = 'Acesso'

	id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id'), primary_key=True)
	id_pagina = db.Column(db.Integer, db.ForeignKey('Pagina.id'), primary_key=True)

	usuario = db.relationship(Usuario)
	pagina = db.relationship(Pagina)

	data_expira = db.Column(db.DateTime, nullable=True)