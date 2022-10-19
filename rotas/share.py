from datetime import timedelta
from http.client import BAD_REQUEST, NOT_FOUND
from init import app, db
from modelos import Acesso, Pagina, Usuario
from rotas.utils import get_campos, validar_dados
from flask_jwt_extended import create_access_token, get_current_user, jwt_required, decode_token
from flask import abort, jsonify, request

@app.post('/api/create-share')
@jwt_required()
def route_create_share():
    pageid = get_campos(int, 'pageid')
    pagina: Pagina = Pagina.query.filter_by(autor=Usuario.logado, id=pageid).first_or_404()

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
    token = get_campos(str, 'claim-token')
    claims = decode_token(token)

    if claims['otp-type'] != 'share':
        abort(BAD_REQUEST)
    
    pagina: Pagina = Pagina.query.get_or_404(claims['otp-page'])
    
    acesso = Acesso(
        usuario=Usuario.logado,
        pagina=pagina,
    )

    db.session.add(acesso)
    db.session.commit()

    return jsonify({
        'pageid': claims['otp-page']
    })