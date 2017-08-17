"""
This script runs the SiaWizard application using a development server.
"""

from os import environ
from Interface import app

import mlapi
#import visionapi
import botapi
#import intentapi
import siacogapi

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')

    try:
        #app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 80
    app.run(HOST, PORT)
