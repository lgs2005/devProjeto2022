from http.client import UNAUTHORIZED

from flask import abort


def int_or_badrequest(str: str):
    try:
        return int(str)
    except ValueError:
        abort(UNAUTHORIZED)