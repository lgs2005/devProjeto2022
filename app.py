import bcrypt
from flask import Flask, make_response, redirect, render_template, request
from banco_de_dados import Usuario, db

app = Flask(',,')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.app_context().push()

db.init_app(app)
db.create_all()

@app.route('/hello')
def hello_world():
    # https://www.youtube.com/watch?v=dwDns8x3Jb4
    return "<img src='https://media1.giphy.com/media/mf8UbIDew7e8g/200.gif'/>" + \
        " ".join(["<p>around the world</p>"] * 200)

def usuario_logado() -> bool:
    email = request.cookies.get('login_email')
    senha = request.cookies.get('login_senha')

    usuario: Usuario = Usuario.query.filter_by(email=email).first()

    return usuario != None and bcrypt.checkpw(senha, usuario.senha)

@app.route('/login')
def login():
    if usuario_logado():
        return

    email, senha = request.args.get('email'), request.args.get('senha')

    if email in ('', None) or senha in ('', None):
        return render_template('login.html')

    usuario: Usuario = Usuario.query.filter_by(email=email).first()    

    if usuario is None:
        return render_template('login.html', erro='Este usuário não existe')
    
    if not bcrypt.checkpw(senha, usuario.pwhash):
        return render_template('login.html', erro='Senha incorreta')
    


@app.route('/registrar')
def registrar():
    email, senha = request.args.get('email'), request.args.get('senha')

    if email in ('', None) or senha in ('', None):
        return render_template('login.html')

    usuario: Usuario = Usuario.query.filter_by(email=email).first()    

    if usuario is None:
        return render_template('login.html', erro='Este usuário já existe')

    pwhash = bcrypt.hashpw(senha, bcrypt.gensalt())

    novo_usuario = Usuario(email, pwhash)
    db.session.add(novo_usuario)
    db.session.commit()

    resposta = make_response('/login')
    resposta.set_cookie('login_email', email)
    resposta.set_cookie('login_senha', senha)

    return resposta
    

@app.route('/')
@app.route('/inicio')
def inicio():
    nome = request.args.get('nome')

    return render_template('inicio.html', nome=nome)
