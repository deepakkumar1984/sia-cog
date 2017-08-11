"""
Routes and views for the flask application.
"""

import os
import shutil
import simplejson as json
import jsonpickle
from flask import jsonify
from flask import request

from Interface import utility, app
from langintent import intentanalyzer
from ml import backgroundproc, pipeline

@app.route('/api/status', methods=['GET'])
def apistatus():
    message = "All Good!"
    code = 200

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/list/<name>', methods=['GET'])
def apilist(name):
    message = "Success"
    code = 200
    try:
        directory = "./data/"
        result = []
        if name == "ml":
            dirs = os.listdir(directory)
            for d in dirs:
                if d == "__vision" or d == "__chatbot" or d == "__intent" or d == "__speech" or d == "__text":
                    continue

                if os.path.isfile(directory + d):
                    continue

                srvpath = directory + d + "/service.json"
                if os.path.exists(srvpath):
                    result.append(utility.getJsonData(srvpath))
        elif name == "vision":
            directory = directory + "__vision/"
            files = os.listdir(directory)
            for f in files:
                if f.endswith(".json"):
                    result.append(utility.getJsonData(directory + f))
        elif name == "bot":
            directory = directory + "__chatbot/"
            dirs = os.listdir(directory)
            for d in dirs:
                if os.path.isfile(directory + d):
                    continue

                botpath = directory + d + "/bot.json"
                if os.path.exists(botpath):
                    result.append(utility.getJsonData(botpath))

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": json.loads(jsonpickle.encode(result, unpicklable=False))})
