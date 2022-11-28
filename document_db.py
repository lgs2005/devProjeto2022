import uuid
import json
import os

from flask import current_app

DOCFILE_FOLDER = 'pages'


def init():
    folder_path = os.path.join(current_app.instance_path, DOCFILE_FOLDER)

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def docfile_path(file_id: str) -> str:
    return os.path.join(
        current_app.instance_path,
        DOCFILE_FOLDER,
        file_id + '.json'
    )

def create_docfile() -> str | None:
    while True:
        file_id = uuid.uuid4().hex
        filepath = docfile_path(file_id)

        try:
            docfile = open(filepath, 'x')
            docfile.write(json.dumps({
                'title': 'Untitled',
                'content': '# teste \n Esta página é um teste.'
            }))

            docfile.close()
            return file_id
        except FileExistsError:
            continue
        except OSError:
            return None