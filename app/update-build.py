import os
import shutil


def update_build():
    os.chdir(os.path.dirname(__file__))

    if os.path.exists('./../static'):
        shutil.rmtree('./../static')

    shutil.move('./build/static', './../')
    shutil.move('./build/index.html', './../static/index.html')


if __name__ == '__main__':
    update_build()
