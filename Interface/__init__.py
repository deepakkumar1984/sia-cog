"""
The flask application package.
"""

from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.trainingstatus = 0