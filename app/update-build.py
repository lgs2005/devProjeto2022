import os
import shutil

def update_build():
	os.chdir(os.path.dirname(__file__))

	if os.path.exists('./../static'):
		shutil.rmtree('./../static')

	shutil.move('./build/static', './../')
	
	if os.path.exists('./../templates/index.html'):
		os.remove('./../templates/index.html')

	shutil.move('./build/index.html', './../templates/index.html')


if __name__ == '__main__':
	update_build()
