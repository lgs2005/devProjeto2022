# proxy for npm

from urllib.request import urlretrieve
import os
import sys
import tarfile

NODE_16_URL = "https://nodejs.org/dist/v16.16.0/node-v16.16.0-linux-x64.tar.xz"
ARCHIVE_NAME = "node-v16.16.0-linux-x64"


def getnode():
    thisdir = os.path.dirname(__file__)
    if thisdir != '':
        os.chdir(thisdir)

    if not os.path.exists('./node16'):
        urlretrieve(NODE_16_URL, './node16.tar.xz')

        with tarfile.open('./node16.tar.xz') as archive:
            archive.extractall()
            os.remove('./node16.tar.xz')
            os.rename('./' + ARCHIVE_NAME, './node16')

    os.environ['PATH'] = thisdir + '/node16/bin/:' + os.environ['PATH']

    npmargs = list(sys.argv)
    npmargs[0] = thisdir + '/node16/bin/npm'
    npmcmd = ' '.join(npmargs)

    os.system(npmcmd)


if __name__ == '__main__':
    getnode()
