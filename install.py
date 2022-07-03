import subprocess, sys

packages = [
	'flask',
	'flask-sqlalchemy',
	'flask-login',
	'flask-bcrypt',
]

if __name__ == "__main__":
	try:
		subprocess.check_call([sys.executable, '-m', 'pip', 'install', *packages])
	except subprocess.CalledProcessError as e:
		print("\n\nNão foi possível instalar:", e)