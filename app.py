from datetime import timedelta
from flask import Flask
from flask_cors import CORS

from database import db
import document_db
import routes.authentication
import routes.documents

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///app.db'
    app.config['JWT_SECRET_KEY'] = '2e1f94b6638147eb8dd0fdbe0c47c20f-3rd-682f814760c048fc83b6ad8ce1121cf9'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    db.init_app(app)
    with app.app_context():
        db.session.execute('PRAGMA FOREIGN_KEYS=ON')
        document_db.init()

    CORS(app, expose_headers=['X-OTP-Update-Bearer'])
    routes.authentication.jwt.init_app(app)

    app.register_blueprint(routes.authentication.bp)
    app.register_blueprint(routes.documents.bp)

    return app