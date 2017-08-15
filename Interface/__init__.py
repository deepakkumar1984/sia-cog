"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import mlapi
import visionapi
import botapi
import intentapi
import siacogapi
import views