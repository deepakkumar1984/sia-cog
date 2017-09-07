import numpy
import pandas
from keras import callbacks
from keras.models import Sequential, model_from_json
from keras import layers
from Interface import dbutility, app
import os

modellist = []
name = ""
jobid = ""

def init(self, name, jobid):
    self.name = name
    self.jobid = jobid

class Histories(callbacks.Callback):
    def on_train_begin(self, logs={}):
        app.trainingstatus = 1
        dbpath = "./data/training_db.json"
        if os.path.exists(dbpath):
            os.remove(dbpath)
        self.losses = []

    def on_train_end(self, logs={}):
        app.trainingstatus = 0
        return

    def on_epoch_begin(self, epoch, logs={}):
        return

    def on_epoch_end(self, epoch, logs={}):
        try:
            list = {}
            for m in logs:
                list[m] = logs[m]

            dbutility.logDeepTraining("mlp", name, epoch, logs.get("loss"), list)
        except Exception as e:
            app.trainingstatus = 0
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
        module = eval("keras.layers.core")
        func = getattr(module, layerName)
        args = {}
        for p in item:
            if p == "name":
                continue
            args[p] = item[p]

        layer = func(**args)
        model.add(layer)

    return model

def buildModel(modelDef, fromFile = False, modelFolder=""):
    if fromFile:
        json_file = open(modelFolder + '/model.out', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights(modelFolder + "/model.hdf5")
    else:
        model = Sequential()
        for m in modelDef['options']['layers']:
            if m['type'] == 'input':
                model.add(layers.Dense(m['val'], input_dim=m['dim'], kernel_initializer=m['init'], activation=m['activation']))
            elif m['type'] == 'dense':
                model.add(layers.Dense(m['val'], kernel_initializer=m['init'], activation=m['activation']))
            elif m['type'] == 'output':
                model.add(layers.Dense(m['val'], kernel_initializer=m['init']))
    

    model_json = model.to_json()
    return model_json

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
    return hist.history

