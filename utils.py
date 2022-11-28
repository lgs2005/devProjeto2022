from http.client import BAD_REQUEST
from operator import itemgetter
from typing import TypeVar

from flask import request, abort


T = TypeVar('T')
def json_fields(field_type: type[T], *fields: str) -> tuple[T, ...]:
    data = request.get_json()
    if not isinstance(data, dict):
        abort(BAD_REQUEST)

    for field in fields:
        if (field not in data) or (not isinstance(data[field], field_type)):
            abort(BAD_REQUEST)
    
    return itemgetter(*fields)(data)