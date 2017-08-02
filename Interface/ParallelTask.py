import threading
import json
from Interface import utility, Pipeline
import uuid
import os
from tinydb import TinyDB, Query
import datetime

def Validate(id, name):
    results = {}
    status = "Completed"
    try:
        with open("./data/" + name + "/service.json") as f:
            srvjson = json.load(f)

        model_type = srvjson["model_type"]
        Pipeline.init(Pipeline, name, model_type)
        pipelinejson = Pipeline.getPipelineData()
        Pipeline.Run()

        for p in pipelinejson:
            if p["module"] == "return_result":
                mlist = p["input"]["module_output"]
                for m in mlist:
                    r = Pipeline.Output(m, to_json=True)
                    results[m] = json.loads(r)
    except Exception as e:
        results["message"] = str(e)
        status = "Error"

    taskdb = TinyDB('./data/' + name + '/jobs_db.json')
    Task = Query()
    taskdb.update({"end": str(datetime.datetime.now()), "status": "Completed", "results": results}, Task.id == id)

def Train(id, name, epoches, batch_size):
    results = {}
    status = "Completed"
    try:
        with open("./data/" + name + "/service.json") as f:
            srvjson = json.load(f)

        model_type = srvjson["model_type"]

        Pipeline.init(Pipeline, name, model_type)
        pipelinejson = Pipeline.getPipelineData()
        Pipeline.ContinueTraining(epoches=epoches, batch_size=batch_size)

        for p in pipelinejson:
            if p["module"] == "return_result":
                mlist = p["input"]["module_output"]
                for m in mlist:
                    r = Pipeline.Output(m, to_json=True)
                    results[m] = json.loads(r)
    except Exception as e:
        results["message"] = str(e)
        status = "Error"

    taskdb = TinyDB('./data/' + name + '/jobs_db.json')
    Task = Query()
    taskdb.update({"end": str(datetime.datetime.now()), "status": status, "results": results}, Task.id == id)

def StartValidateThread(name):
    id = str(uuid.uuid4())
    taskdb = TinyDB('./data/' + name + '/jobs_db.json')
    taskdb.insert({"id": id, "start": str(datetime.datetime.now()), "end": "", "status": "Started", "results": []})
    t = threading.Thread(target=Validate, args=(id, name))
    t.start()
    return id

def StartTrainThread(name, epoches, batch_size):
    id = str(uuid.uuid4())
    taskdb = TinyDB('./data/' + name + '/jobs_db.json')
    taskdb.insert({"id": id, "start": str(datetime.datetime.now()), "end": "", "status": "Started", "results": []})
    t = threading.Thread(target=Train, args=(id, name, epoches, batch_size))
    t.start()
    return id

def GetStatus(name, id):
    taskdb = TinyDB('./data/' + name + '/jobs_db.json')
    Task = Query()
    return taskdb.search(Task.id == id)

def UpdateTaskError(name, id, message):
    taskdb = TinyDB('./data/' + name + '/jobs_db.json')
    Task = Query()
    results = {"message": message}

    taskdb.update({"end": str(datetime.datetime.now()), "status": "Error", "results": results}, Task.id == id)