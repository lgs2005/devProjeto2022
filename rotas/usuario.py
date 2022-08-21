import re

from flask import jsonify, redirect, render_template, request
from flask_login import current_user, login_user, logout_user
from init import app, bcrypt, db
from modelos import Usuario

from rotas.utils import api_requer_login, validar_objeto

emailPattern = re.compile(
    "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")


@app.route("/login", methods=["GET"])
def rota_login():
    """
    Rota login utilizada para renderizar o HTML.

    Template utilizado: 'login.html'.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """

    if current_user.is_authenticated:
        return redirect("/inicio")
    else:
        return render_template("login.html")


@app.route("/api/login", methods=["POST"])
def rota_api_login():
    """Rota para login e regitro de usuários.
    Para login, recebe email e senha.
    Para registro, recebe também o nome.

    Foi feita uma separação entre erros que o usuário pode cometer; o
    JavaScript ficou responsável por aqueles erros mais "genéricos":
        -> Email vazio;
        -> Senha vazia;
        -> Nome de usuário vazio;
        -> Email inválido (com base em um padrão web).

    O Python (back-end) ficou responsável por informações que só podem
    ser validadas após o envio do formulário:
        -> Usuário já existe (email já cadastrado no banco de dados);

    Caso o usuário já estiver logado, mas enviar informações de login válidas,
    sua sessão será sobrescrita.

    Returns:
        Response (jsonify): resposta em json contendo sucesso e erro.
    """

    dados = validar_objeto(request.get_json(), {
        'email': str,
        'senha': str,
    })

    sucesso = False
    usuario_final = None
    erro = None
    errtarget = None;

    # se não for especificado, é False
    if not dados.get('registro', False):
        usuario: Usuario = Usuario.query.filter_by(
            email=dados['email']).first()

        if usuario == None:
            erro, errtarget = "Este usuário não existe", "email"
        elif not bcrypt.check_password_hash(usuario.pwhash, dados['senha']):
            erro, errtarget = "Senha incorreta", "senha"
        else:
            sucesso = True
            usuario_final = usuario
    else:
        # se for um registro, precisamos validar informações extras, o nome do usuario
        dados = validar_objeto(dados, {
            'nome': str,
        })

        if Usuario.query.filter_by(email=dados['email']).first() != None:
            erro, errtarget = "Este usuário já existe", "email"
        elif (not emailPattern.fullmatch(dados['email'])):
            erro, errtarget = "Email inválido", "email"
        else:
            pwhash = bcrypt.generate_password_hash(dados['senha']) \
                .decode('utf-8', 'ignore')

            novo_usuario = Usuario(
                nome=dados['nome'],
                email=dados['email'],
                pwhash=pwhash,
            )

            db.session.add(novo_usuario)
            db.session.commit()

            sucesso = True
            usuario_final = novo_usuario

    if sucesso and usuario_final != None:
        if current_user.is_authenticated:
            logout_user()
        login_user(usuario_final)

    return jsonify({
        'sucesso': sucesso,
        'erro': erro,
        'errtarget': errtarget,
    })


@app.route("/api/auth/login", methods=['POST'])
def auth_login():
	dados = validar_objeto(request.get_json(), {
		'email': str,
		'password': str,
	})

	sucess = False
	erro = None
	errtarget = None

	usuario: Usuario = Usuario.query.filter_by(
		email=dados['email']).first()

	if usuario == None:
		erro, errtarget = "Este usuário não existe", "email"
	elif not bcrypt.check_password_hash(usuario.pwhash, dados['password']):
		erro, errtarget = "Senha incorreta", "password"
	else:
		sucess = True
	
	if sucess and usuario != None:
		if current_user.is_authenticated:
			logout_user()
		login_user(usuario)

	return jsonify({
		'sucess': sucess,
		'error': erro,
		'err_target': errtarget,
	})


@app.route("/api/auth/register", methods=['POST'])
def auth_register():
	dados = validar_objeto(request.get_json(), {
        'email': str,
        'senha': str,
		'nome': str
    })

	sucesso = False
	erro = None
	errtarget = None

	if Usuario.query.filter_by(email=dados['email']).first() != None:
		erro, errtarget = "Este usuário já existe", "email"
	elif (not emailPattern.fullmatch(dados['email'])):
		erro, errtarget = "Email inválido", "email"
	else:
		pwhash = bcrypt.generate_password_hash(dados['senha']) \
			.decode('utf-8', 'ignore')

		novo_usuario = Usuario(
			nome=dados['nome'],
			email=dados['email'],
			pwhash=pwhash,
		)

		db.session.add(novo_usuario)
		db.session.commit()

		sucesso = True

	if sucesso and novo_usuario != None:
		if current_user.is_authenticated:
			logout_user()
		login_user(novo_usuario)

	return jsonify({
		'sucesso': sucesso,
		'erro': erro,
		'errtarget': errtarget,
	})


@app.route("/logout", methods=["GET"])
def rota_logout():
    """
    Rota para logout do usuário.

    Returns:
        redirect -> `/`
    """
    logout_user()
    return redirect('/')


@app.route("/api/alterar-senha", methods=["POST"])
@api_requer_login
def rota_api_alterar_senha():
    erro = None
    dados = validar_objeto(request.get_json(), {
        'senha': str,
        'novaSenha': str,
    })

    if not bcrypt.check_password_hash(current_user.pwhash, dados['senha']):
        erro = "Senha incorreta"
    else:
        nova_pwhash = bcrypt.generate_password_hash(dados['novaSenha']) \
            .decode('utf-8', 'ignore')

        current_user.pwhash = nova_pwhash
        db.session.commit()

    return {
        'ok': erro == None,
        'erro': erro,
        'errtarget': "senha", # só temos erros aqui, então...
    }
        