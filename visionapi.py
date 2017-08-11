"""
Routes and views for the flask application.
"""

import os
import shutil

import simplejson as json
from flask import jsonify
from flask import request

from Interface import app, utility
from vis import objcls, objdet, cvmgr


@app.route('/api/vis/create', methods=['POST'])
def visioncreate():
    message = "Success"
    code = 200
    try:
        rjson = json.loads(request.json)
        name = rjson["name"]
        directory = "./data/__vision"
        file = directory + "/" + name + ".json"
        if not os.path.exists(directory):
            os.makedirs(directory)
            json_string = json.dumps(request.json)
            file = open(file, "w")
            file.write(json_string)
            file.close()
        else:
            code = 1001
            message = "Service already exists!"

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/vis/update/<name>', methods=['POST'])
def visionupdate(name):
    message = "Success"
    code = 200
    try:
        directory = "./data/__vision"
        file = directory + "/" + name + ".json"
        if not os.path.exists(directory):
            code = 1001
            message = "Service does not exists!"
        else:
            json_string = json.dumps(request.json)
            file = open(file, "w")
            file.write(json_string)
            file.close()

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/vis/delete/<name>', methods=['POST'])
def visiondelete(name):
    message = "Success"
    code = 200
    try:
        directory = "./data/__vision"
        file = directory + "/" + name + ".json"
        if not os.path.exists(file):
            code = 1001
            message = "Service does not exists!"
        else:
            shutil.rmtree(directory)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/vis/predict/<name>', methods=['POST'])
def visionpredict(name):
    message = "Success"
    code = 200
    try:
        data = json.loads(request.data)
        directory = "./data/__vision"
        file = directory + "/" + name + ".json"
        servicejson = utility.getJsonData(file)
        result = {}
        imagepath = data['imagepath']

        if servicejson["type"] == "cls":
            target_x = servicejson['options']['target_size_x']
            target_y = servicejson['options']['target_size_y']
            model_name = servicejson['options']['model']
            model = objcls.loadModel(model_name, target_x, target_y)
            result = objcls.predict(imagepath, target_x, target_y, model_name, model)
        elif servicejson["type"] == "det":
            model_name = servicejson['options']['model']
            isgpu = servicejson['options']['gpu']
            model = objdet.loadModel(model_name, 10, isgpu)
            result = objdet.predict(imagepath, model)
        elif servicejson["type"] == "face":
            result = cvmgr.detectfaces(imagepath)
        elif servicejson["type"] == "ocr":
            preprocess = "thresh"
            if "preprocess" in servicejson["options"]:
                preprocess = servicejson["options"]["preprocess"]

            result = cvmgr.extracttext(imagepath, preprocess)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/vis/download/<name>', methods=['POST'])
def downloadmodels(name):
    objcls.loadModel(name, 224, 224)

