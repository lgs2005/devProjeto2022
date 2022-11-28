from datetime import datetime, timedelta
from http.client import CONFLICT, FORBIDDEN

from flask import Blueprint, Response, abort, jsonify
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt,
                                jwt_required)
from sqlalchemy import select

from database import User, db
from utils import json_fields

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
jwt = JWTManager()


@bp.post('/login')
def route_login():
    '''Rota responsável por login de usuários
    Returns:
        200 OK: Os dados do usuário, com o token de acesso
        404 NOT FOUND: Este usuário não existe
        403 FORBIDDEN: Senha incorreta
    '''

    email, password = json_fields(str, 'email', 'password')
    user: User = db.one_or_404(select(User).filter_by(email=email))

    if not check_password_hash(user.pwhash, password):
        abort(FORBIDDEN)

    token = create_access_token(identity=user.id)
    response = jsonify(user.data())
    response.headers.set('X-OTP-Update-Bearer', token)

    return response


@bp.post('/register')
def route_register():
    ''''''

    name, email, password = json_fields(str, 'name', 'email', 'password')

    if db.session.scalar(select(User).filter_by(email=email)) != None:
        abort(CONFLICT)

    pwhash = generate_password_hash(password).decode('UTF-8')
    new_user = User(
        name=name,
        email=email,
        pwhash=pwhash,
    )

    db.session.add(new_user)
    db.session.commit()

    token = create_access_token(identity=new_user.id)
    response = jsonify(new_user.data())
    response.headers.set('X-OTP-Update-Bearer', token)

    return response


@jwt.user_lookup_loader
def load_user(_jwt_header, jwt_data):
    return db.session.get(User, jwt_data['sub'])


@bp.after_app_request
def refresh_jwt(response: Response):
    try:
        expire_timestamp = get_jwt()['exp']
        refresh_timestamp = datetime.timestamp(
            datetime.now() + timedelta(minutes=15))

        if refresh_timestamp > expire_timestamp:
            new_token = create_access_token(identity=User.current().id)
            response.headers.set('X-OTP-Atualizar-Token', new_token)

        return response
    except (RuntimeError, KeyError):
        return response


@bp.get('/user')
@jwt_required()
def route_user():
    return jsonify(User.current().data())

# TODO: rota para alterar dados do usuário ?
