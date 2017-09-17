import numpy
import pandas
import keras
from keras import callbacks
from keras.models import Sequential, model_from_json
from keras import layers
from Interface import app, projectmgr
import simplejson as json

modellist = []
name = ""
jobid = ""

def init(self, name, jobid):
    self.name = name
    self.jobid = jobid

class Histories(callbacks.Callback):
    def on_train_begin(self, logs={}):
        app.trainingstatus = 1
        self.losses = []

    def on_train_end(self, logs={}):
        app.trainingstatus = 0
        projectmgr.ClearCurrentTraining(jobid)

        return

    def on_epoch_begin(self, epoch, logs={}):
        return

    def on_epoch_end(self, epoch, logs={}):
        try:
            list = {}
            for m in logs:
                list[m] = logs[m]

            projectmgr.LogCurrentTraining(jobid, epoch, logs.get("loss"))
        except Exception as e:
            app.trainingstatus = 0
            projectmgr.ClearCurrentTraining(jobid)
            raise e
        return

    def on_batch_begin(self, batch, logs={}):
        return

    def on_batch_end(self, batch, logs={}):
        return

def createModel(modelDef):
    model = Sequential()
    for item in modelDef:
        layerName = item["name"]
        module = eval("keras.layers." + item["cat"])
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

def buildModel(modelDef):
    model = Sequential()
    for m in modelDef['layers']:
        if m['type'] == 'input':
            model.add(
                layers.Dense(m['val'], input_dim=m['dim'], kernel_initializer=m['init'], activation=m['activation']))
        elif m['type'] == 'dense':
            model.add(layers.Dense(m['val'], kernel_initializer=m['init'], activation=m['activation']))
        elif m['type'] == 'output':
            model.add(layers.Dense(m['val'], kernel_initializer=m['init']))

    return model

def Train(model, X, Y, weightpath, epoch=32, batch_size=32, validation_split = None):
    if type(X) is pandas.DataFrame:
        X = X.values

    if type(Y) is pandas.DataFrame:
        Y = Y.values

    seed = 7
    numpy.random.RandomState(seed)
    hist = Histories()
    if validation_split is None:
        hist = model.fit(X, Y, epochs=epoch, batch_size=batch_size, verbose=1, callbacks=[hist])
    else:
        hist = model.fit(X, Y, validation_split=validation_split, epochs=epoch, batch_size=batch_size, verbose=1, callbacks=[hist])


    model.save_weights(weightpath)
    result = {"epoches": hist.epoch, "metrices": hist.history}
    return result

