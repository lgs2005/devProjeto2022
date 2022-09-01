import os
import shutil

def build():
	os.chdir(os.path.dirname(__file__))

	# if os.system('npm run build') != 0:
	# 	return

	if os.path.exists('./../static'):
		shutil.rmtree('./../static')

	shutil.move('./build/static', './../')
	shutil.move('./build/index.html', './../static/index.html')


if __name__ == '__main__':
	build()