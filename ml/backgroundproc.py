import datetime
import json
import threading
import uuid
from Interface import projectmgr
from ml import pipeline

def Validate(id, name):
    results = {}
    status = "Completed"
    message = "Completed"
    try:
        srvjson = json.loads(projectmgr.GetService(name, "ml").servicedata)

        model_type = srvjson["model_type"]
        pipeline.init(pipeline, name, model_type, id)
        pipelinejson = pipeline.getPipelineData()
        pipeline.Run()

        for p in pipelinejson:
            if p["module"] == "return_result":
                mlist = p["input"]["module_output"]
                for m in mlist:
                    r = pipeline.Output(m)
                    results[m] = json.loads(r)

    except Exception as e:
        results["message"] = pipeline.lastpipeline + ": " + str(e)
        message = str(e)
        status = "Error"

    projectmgr.EndJob(id, status, message, json.dumps(results))

def Train(id, name, epoches, batch_size):
    results = {}
    status = "Completed"
    message = "Completed"
    try:
        srvjson = json.loads(projectmgr.GetService(name, "ml").servicedata)
        model_type = srvjson["model_type"]
        pipeline.init(pipeline, name, model_type, id)
        pipelinejson = pipeline.getPipelineData()
        pipeline.ContinueTraining(epoches=epoches, batch_size=batch_size)

        for p in pipelinejson:
            if p["module"] == "return_result":
                mlist = p["input"]["module_output"]
                for m in mlist:
                    r = pipeline.Output(m)
                    results[m] = json.loads(r)
    except Exception as e:
        results["message"] = pipeline.lastpipeline + ": " + str(e)
        message = str(e)
        status = "Error"

    projectmgr.EndJob(id, status, message, json.dumps(results))

def StartValidateThread(name):
    id = projectmgr.StartJob(name, "ml", 0);
    t = threading.Thread(target=Validate, args=(id, name))
    t.start()
    return id

def StartTrainThread(name, epoches, batch_size):
    id = projectmgr.StartJob(name, "ml", epoches);
    t = threading.Thread(target=Train, args=(id, name, epoches, batch_size))
    t.start()
    return id
