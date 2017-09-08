import simplejson as json
from flask import jsonify, request
from dateutil import parser
from Interface import utility, app, dataanalyzer, sysinfo, projectmgr, logmgr
import jsonpickle

@app.route('/api/status', methods=['GET'])
def apistatus():
    message = "All Good!"
    code = 200

    return jsonify({"statuscode": code, "message": message})

@app.route('/api/server/<infotype>', methods=['GET'])
def systeminfo(infotype):
    message = "Success"
    code = 200
    try:
        result = {}
        if infotype == "info":
            result = sysinfo.getSystemInfo()
        elif infotype == "cpu":
            result = sysinfo.getCPUUsage()
        elif infotype == "gpu":
            result = sysinfo.getGPUUsage()
    except Exception as e:
        message = str(e)
        code = 500

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/list/<srvtype>', methods=['GET'])
def apilist(srvtype):
    message = "Success"
    code = 200
    result = []
    try:
        services = projectmgr.GetServices(srvtype)
        for s in services:
            result.append(json.loads(s.servicedata));

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/list/<srvtype>/<srvname>', methods=['GET'])
def apilistwithname(srvtype, srvname):
    message = "Success"
    code = 200
    result = []
    try:
        service = projectmgr.GetService(srvtype, srvname)
        if service is None:
            raise Exception("Service API not found")

        result = json.loads(service.servicedata)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/jobs/<id>', methods=['GET'])
def jobswithid(id):
    message = "Started"
    result = []
    code = 200
    try:
        job = projectmgr.GetJob(id)
        if not job.result is None:
            result = json.loads(job.result)

    except Exception as e:
        code = 500
        message = str(e)

    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/data/info', methods=['POST'])
def databasicinfo():
    message = "Success"
    code = 200
    result = []
    try:
        rjson = request.json
        if not "name" in rjson:
            raise Exception("Please provide name of the service")

        if not "filename" in rjson:
            raise Exception("Please provide filename")

        columns = None
        count = 5
        if "columns" in rjson:
            columns = rjson["columns"]

        if "count" in rjson:
            count = rjson["count"]

        result = dataanalyzer.basic_info(rjson["name"], rjson["filename"], columns, count)

    except Exception as e:
        message = str(e)
        code = 500
    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/data/plot', methods=['POST'])
def dataplot():
    message = "Success"
    code = 200
    result = []
    try:
        rjson = request.json
        utility.validateParam(rjson, "name")
        utility.validateParam(rjson, "filename")
        utility.validateParam(rjson, "method")
        options = utility.getVal(rjson, "options")
        result = dataanalyzer.plot(rjson["name"], rjson["filename"], rjson["method"], options)

    except Exception as e:
        message = str(e)
        code = 500
    return jsonify({"statuscode": code, "message": message, "result": result})

@app.route('/api/logs/pred', methods=['POST'])
def predlogs():
    message = "Success"
    code = 200
    result = []
    try:
        rjson = request.get_json()
        utility.validateParam(rjson, "category")
        utility.validateParam(rjson, "servicename")
        utility.validateParam(rjson, "status")
        utility.validateParam(rjson, "start")
        utility.validateParam(rjson, "end")
        start = parser.parse(rjson["start"] + " 00:00")
        end = parser.parse(rjson["end"] + " 23:59")

        logs = logmgr.GetLogs(rjson["servicename"], rjson["category"], start, end, rjson["status"])
        result = jsonpickle.encode(logs, unpicklable=False)

    except Exception as e:
        message = str(e)
        code = 500
    return jsonify({"statuscode": code, "message": message, "result": result})