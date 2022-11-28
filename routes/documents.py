from datetime import datetime
from http.client import INTERNAL_SERVER_ERROR

from flask import Blueprint, jsonify, abort
from flask_jwt_extended import jwt_required
from sqlalchemy import select

from database import Folder, User, db, Page
from utils import json_fields
from document_db import create_docfile


bp = Blueprint('documents', __name__, url_prefix='/api/docs')


@bp.post('/folder/new')
@jwt_required()
def route_create_folder():
    ''''''

    name = json_fields(str, 'name')
    new_folder = Folder(
        name=name,
        user=User.current(),
    )

    db.session.add(new_folder)
    db.session.commit()

    return jsonify(new_folder.data())


@bp.post('/<int:folder_id>/new')
@jwt_required()
def route_create_doc(folder_id: int):
    folder: Folder = db.get_or_404(Folder, folder_id)
    name = json_fields(str, 'name')
    docfile = create_docfile()

    if docfile == None:
        abort(INTERNAL_SERVER_ERROR)

    new_doc = Page(
        author=User.current(),
        folder=folder,
        name=name,
        file=docfile,
        creation_date=datetime.utcnow(),
        deletion_date=None,
    )

    db.session.add(new_doc)
    db.session.commit()

    return jsonify(new_doc.data())


@bp.get('/doclist')
@jwt_required()
def route_list_all_docs():
    folders: list[Folder] = db.session.scalars(
        select(Folder)
        .filter_by(user=User.current())
    ).all()

    folder_data = [
        {
            **f.data(),
            'pages': [
                p.data()
                for p in f.pages
            ]
        }
        for f in folders
    ]
    
    return jsonify(folder_data)


@bp.get('/<int:folder_id>')
@jwt_required()
def route_list_folder_docs(folder_id: int):
    return jsonify(db.get_or_404(Folder, folder_id).data())
