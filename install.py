import subprocess, sys

packages = [
	'flask',
	'flask-sqlalchemy',
	'flask-login',
	'flask-bcrypt',
]

def install():
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', *packages])

if __name__ == "__main__":
	try:
		install()
	except subprocess.CalledProcessError as e:
		print("Não foi possível instalar:", e)