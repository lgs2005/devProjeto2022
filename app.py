from distutils.log import error
from flask import Flask, request
from banco_de_dados import db

app = Flask(',,')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://./test.db'


db.init_app(app)

@app.route('/')
def hello_world():
    # https://www.youtube.com/watch?v=dwDns8x3Jb4
    return "<img src='https://media1.giphy.com/media/mf8UbIDew7e8g/200.gif'/>" + \
        " ".join(["<p>around the world</p>"] * 200)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        # TODO: página para login
        return hello_world()
    elif request.method == 'POST':
        nome, senha = request.form['nome'], request.form['senha']
        registrar = request.form['registrar']

        if (
            type(nome) == str and
            type(senha) == str
        ):
            if registrar == True:
                # registrar usuário
                pass
            elif False: # login_valido(nome, senha):
                # logar usuario
                pass
            else:
                error = "Este nome/senha não existe."
        else:
            error = "Valores inválidos"
                


