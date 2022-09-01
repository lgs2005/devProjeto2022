import subprocess, sys

packages = [
	'flask',
	'flask-sqlalchemy',
	'flask-jwt-extended',
	'flask-bcrypt',
	'flask-cors',
]

if __name__ == "__main__":
	try:
		subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', *packages])
	except subprocess.CalledProcessError as e:
		print("\n\nNão foi possível instalar:", e)