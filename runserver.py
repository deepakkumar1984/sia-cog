"""
This script runs the SiaWizard application using a development server.
"""

from os import environ
from Interface import app
import os

def createDataFolder():
    basefolder = "./data/"
    if not os.path.exists(basefolder + "__vision"):
        os.makedirs(basefolder + "__vision")
    if not os.path.exists(basefolder + "__intent"):
        os.makedirs(basefolder + "__intent")
    if not os.path.exists(basefolder + "__chatbot"):
        os.makedirs(basefolder + "__chatbot")
    if not os.path.exists(basefolder + "__text"):
        os.makedirs(basefolder + "__text")

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    createDataFolder()
    try:
        #app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 80
    app.run(HOST, PORT)
