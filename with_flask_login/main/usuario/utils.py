from typing import Union
import bcrypt
from flask import  request

from modelos import Usuario


COOKIE_EMAIL = 'login_email'
COOKIE_SENHA = 'login_senha'

def usuario_logado() -> Union[Usuario, None]:
    """
    Retorna o usuário (classe Usuario) que está acessando essa rota.

    Se não existir um usuário logado ou os cookies email e/ou senha
    não existirem, será retornado None.
    """
    email = request.cookies.get(COOKIE_EMAIL)
    senha = request.cookies.get(COOKIE_SENHA)

    if None or '' in (email, senha): return None 
    # Não existem cookies de login, ou seja, usuário não está logado

    usuario = Usuario.query.filter_by(email=email).first()
    senha_bytes = bytes(senha, 'utf-8')

    if usuario == None: return None
    # Não existe um usuário com o email dos cookies

    if bcrypt.checkpw(senha_bytes, usuario.pwhash) == False: return None
    # Senha inválida

    return Usuario
    # SUCESSO
