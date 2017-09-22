"""
Routes and views for the flask application.
"""

from flask import jsonify
from flask import request
from datetime import datetime
from Interface import app, utility, logmgr, projectmgr, constants
from vis import objcls, objdet, cvmgr


@app.route('/api/vis/create', methods=['POST'])
def visioncreate():
    message = "Success"
    code = 200
    try:
        rjson = request.get_json()
        name = rjson["servicename"]
        projectmgr.UpsertService(name, constants.ServiceTypes.Vision, rjson)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/vis/update/<name>', methods=['POST'])
def visionupdate(name):
    message = "Success"
    code = 200
    try:
        rjson = request.get_json()
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.Vision)
        projectmgr.UpsertService(name, constants.ServiceTypes.Vision, rjson)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/vis/delete/<name>', methods=['POST'])
def visiondelete(name):
    message = "Success"
    code = 200
    try:
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.Vision)
        projectmgr.DeleteService(name, constants.ServiceTypes.Vision)
    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/vis/predict/<name>', methods=['POST'])
def visionpredict(name):
    message = "Success"
    code = 200
    start = datetime.now()
    try:
        data = request.get_json()
        projectmgr.ValidateServiceExists(name, constants.ServiceTypes.Vision)
        servicejson = utility.getServiceJson(name, constants.ServiceTypes.Vision)
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

        logmgr.LogPredSuccess(name, constants.ServiceTypes.Vision, start)
    except Exception as e:
        code = 500
        message = str(e)
        logmgr.LogPredError(name, constants.ServiceTypes.Vision, start, message)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/vis/download/<name>', methods=['POST'])
def downloadmodels(name):
    objcls.loadModel(name, 224, 224)

