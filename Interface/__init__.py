"""
The flask application package.
"""

from flask import Flask
from flask_cors import CORS, cross_origin
import numpy
import jsonpickle
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.trainingstatus = 0

class NumpyFloatHandler(jsonpickle.handlers.BaseHandler):
    """
    Automatic conversion of numpy float  to python floats
    Required for jsonpickle to work correctly
    """
    def flatten(self, obj, data):
        """
        Converts and rounds a Numpy.float* to Python float
        """
        return round(obj,6)

jsonpickle.handlers.registry.register(numpy.int, NumpyFloatHandler)
jsonpickle.handlers.registry.register(numpy.int32, NumpyFloatHandler)
jsonpickle.handlers.registry.register(numpy.int64, NumpyFloatHandler)
jsonpickle.handlers.registry.register(numpy.float, NumpyFloatHandler)
jsonpickle.handlers.registry.register(numpy.float32, NumpyFloatHandler)
jsonpickle.handlers.registry.register(numpy.float64, NumpyFloatHandler)