"""
This script runs the SiaWizard application using a development server.
"""

from os import environ
from Interface import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        #app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
