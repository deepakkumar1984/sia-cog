"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import Interface.views
import Interface.mlapi
import Interface.visionapi
import Interface.intentapi
