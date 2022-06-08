import flask_login
from modelos import Usuario

class _UserType(Usuario):
    is_authenticated: bool

current_user: _UserType