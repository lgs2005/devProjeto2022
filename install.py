import subprocess
import sys

packages = [
    'flask',
    'flask-sqlalchemy',
    'flask-jwt-extended',
    'flask-bcrypt',
    'flask-cors',
    'sqlalchemy2-stubs',
]

if __name__ == '__main__':
    try:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', *packages])
    except subprocess.CalledProcessError as e:
        print('\n\nNão foi possível instalar.')
        print(e)
