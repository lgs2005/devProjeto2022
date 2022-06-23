from flask import render_template, redirect
from flask_login import current_user


def rota_default():
    """
    Rota default.
    Esta rota só existe para o usuário poder acessar o site normalmente 
    sem ter "POR FAVOR ENTRE EM SUA CONTA PARA VISUALIZAR ESTA PÁGINA" 
    na sua primeira vez.
    """
    return render_template('inicio.html') if current_user.is_authenticated else redirect('login')


def adicionar_rotas():
    return {
        '/': rota_default,
    }
