from flask import Blueprint
from flask_jwt_extended import jwt_required

from database import Page, User
from utils import json_fields

bp = Blueprint('content', __name__, url_prefix='/api/content')
