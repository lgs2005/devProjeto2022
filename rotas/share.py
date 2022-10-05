from datetime import timedelta
from http.client import BAD_REQUEST, NOT_FOUND
from init import app, db
from modelos import Acesso, Pagina, Usuario
from rotas.utils import validar_dados
from flask_jwt_extended import create_access_token, get_current_user, jwt_required, decode_token
from flask import abort, jsonify, request

@app.post('/api/create-share')
@jwt_required()
def route_create_share():
    usuario: Usuario = get_current_user()
    dados = validar_dados(request.get_json(), {
        'pageid': int,
    })

    pagina: Pagina = Pagina.query\
        .filter_by(id_autor=usuario.id, id=dados['pageid']).first()

    if pagina == None:
        abort(NOT_FOUND)

    token = create_access_token(
        -1,
        expires_delta=timedelta(days=5),
        additional_claims={
            'otp-type': 'share',
            'otp-page': pagina.id,
        }
    )

    return jsonify({
        'token': token,
    })

@app.post('/api/claim-share')
@jwt_required()
def route_claim_share():
    usuario: Usuario = get_current_user()
    dados = validar_dados(request.get_json(), {
        'claim-token': str,
    })

    claims = decode_token(dados['claim-token'])
    print(claims)

    if claims['otp-type'] != 'share':
        abort(BAD_REQUEST)
    
    pagina: Pagina = Pagina.query.get_or_404(claims['otp-page'])
    
    acesso = Acesso(
        id_usuario = usuario.id,
        id_pagina = pagina.id,
    )

    db.session.add(acesso)
    db.session.commit()

    return ''