import numpy
import pandas
import mxnet as mx
from Interface import app, projectmgr
import simplejson as json
from datetime import time
import os

modellist = []
name = ""
jobid = ""

def log_custom_metrics(period):
    def _callback(param):
        """The checkpoint function."""
        if param.nbatch % period == 0 and param.eval_metric is not None:
            name_value = param.eval_metric.get_name_value()
            for name, value in name_value:
                print('Iter[%d] Batch[%d] Train-%s=%f', param.epoch, param.nbatch, name, value)
            param.eval_metric.reset()
    return _callback

class log_speed(object):
    def __init__(self, batch_size, frequent=50, auto_reset=True):
        self.batch_size = batch_size
        self.frequent = frequent
        self.init = False
        self.tic = 0
        self.last_count = 0
        self.auto_reset = auto_reset

    def __call__(self, param):
        """Callback to Show speed."""
        count = param.nbatch
        if self.last_count > count:
            self.init = False
        self.last_count = count

        if self.init:
            if count % self.frequent == 0:
                speed = self.frequent * self.batch_size / (time.time() - self.tic)
                print("Iter[%d] Batch [%d]\tSpeed: %.2f samples/sec", param.epoch, count, speed)

                self.tic = time.time()
        else:
            self.init = True
            self.tic = time.time()

def init(self, name, jobid):
    self.name = name
    self.jobid = jobid

def generateFinalTrainingResult():
    result = {}
    return result

def createModel(modelDef):
    model = mx.gluon.nn.Sequential()

    with model.name_scope():
        for item in modelDef:
            layerName = item["name"]
            module = eval("mx.gluon" + item["cat"])
            func = getattr(module, layerName)
            args = {}
            for p in item["options"]:
                value = item["options"][p]
                if type(value) is list:
                    value = tuple(value)
                args[p] = value

            layer = func(**args)
            model.add(layer)

    return model

def Train(model, X, Y, projectpath, options, epoch=32, batch_size=32, X_test=None, Y_test=None, useGpu=False, gpuList=[0], more=False):
    if useGpu:
        gpuContextList = []
        for g in gpuList:
            gpuContextList.append(mx.gpu(g))

        module = mx.mod.Module(model, context=[gpuContextList])
    else:
        module = mx.mod.Module(model, context=mx.cpu())

    if type(X) is pandas.DataFrame:
        X = mx.nd.array(X.values)

    if type(Y) is pandas.DataFrame:
        Y = mx.nd.array(Y.values)

    train_iter = mx.io.NDArrayIter(X, Y, batch_size)
    if more:
        module.load_params(projectpath + "\weights.params")
        module.load_optimizer_states(projectpath + "\woptimizer_states.json")

    if X_test is None:
        module.fit(train_iter, None, num_epoch=epoch, eval_metric=options["scoring"],
                          epoch_end_callback=log_custom_metrics(1), batch_end_callback=log_speed(1,50),
                          optimizer=options["optimizer"])
    else:
        if not X_test is None & type(X_test) is pandas.DataFrame:
            X_test = mx.nd.array(X_test.values)

        if not Y_test is None & type(Y_test) is pandas.DataFrame:
            Y_test = mx.nd.array(Y_test.values)
        test_iter = mx.io.NDArrayIter(X_test, Y_test, batch_size)

        module.fit(train_iter, test_iter, num_epoch=epoch, eval_metric=options["scoring"],
                   epoch_end_callback=log_custom_metrics(1), batch_end_callback=log_speed(1, 50),
                   optimizer=options["optimizer"])

    module.save_params(projectpath + "\weights.params")
    module.save_optimizer_states(projectpath + "\woptimizer_states.json")

    result = generateFinalTrainingResult()

    return result
