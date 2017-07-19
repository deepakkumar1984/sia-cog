import numpy
import keras
import json
import datetime
import os
import csv
import pandas
from pandas import read_csv
from Interface import utility
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn import preprocessing
from tinydb import TinyDB, Query

class LossHistory(keras.callbacks.Callback):
    modelFolder = ""
    id = ""

    def init(self, jobid, path):
        self.modelFolder = path
        self.id = jobid
        self.historydb = TinyDB(self.modelFolder + "/history_db.json")
        self.taskdb = TinyDB(self.modelFolder + "/task_db.json")
    
    def saveLogs(self, epoch, log):
        log['taskid'] = self.id
        self.historydb.insert(log)

    def on_epoch_end(self, epoch, logs={}):
        self.saveLogs(epoch, logs)

    def on_train_begin(self, logs=None):
        self.taskdb.insert({"id": self.id, "start": str(datetime.datetime.now()), "end": "", "status": "Started"})

    def on_train_end(self, logs=None):
        Task = Query()
        self.taskdb.update({"end": str(datetime.datetime.now()), "status": "Completed"}, Task.id == self.id)

def buildModel(modelDef):
    model = Sequential()
    print(modelDef['model'])
    for m in modelDef['model']:
        if m['type'] == 'input':
            model.add(Dense(m['val'], input_dim=m['dim'], kernel_initializer=m['init'], activation=m['activation']))   
        elif m['type'] == 'dense':
            model.add(Dense(m['val'], kernel_initializer=m['init'], activation=m['activation']))
        elif m['type'] == 'output':
            model.add(Dense(m['val'], kernel_initializer=m['init']))
    
    model.compile(loss=modelDef['trainingparam']['loss'], optimizer=modelDef['trainingparam']['optimizer'], metrics=modelDef['scoring'])
    return model

def Evalute(id, modelDef, filename, modelFolder):
    if modelDef['dataset']['column_header'] == True:
        dataframe = read_csv(filename, delim_whitespace=modelDef['dataset']['delim_whitespace'])
    else:
        dataframe = read_csv(filename, delim_whitespace=modelDef['dataset']['delim_whitespace'], header=None)
    
    if modelDef['dataset']['colsdefined'] == True:
        X_frame = dataframe[modelDef['xcols']]
        Y_frame = dataframe[modelDef['ycols']]
        X = X_frame.values
        Y = Y_frame.values
    else:
        array = dataframe.values
        rsplit = modelDef['dataset']['xrange'].split(":")
        X = array[:, int(rsplit[0]):int(rsplit[1])]
        Y = array[:, modelDef['dataset']['yrange']]
    
    X = X.astype(numpy.float32)
    Y = Y.astype(numpy.float32)
    X = utility.scaleData(modelDef['preprocessdata'], X)
    seed = 7
    numpy.random.RandomState(seed)
    #numpy.random.seed(seed)
    kfold = KFold(n_splits=10, random_state=seed)
    model = buildModel(modelDef)
    history = LossHistory()
    history.init(id, modelFolder)
    model.fit(X, Y, epochs=modelDef['trainingparam']['epoches'], batch_size=modelDef['trainingparam']['batch_size'], verbose=1, callbacks=[history])
    scores = model.evaluate(X, Y, verbose=0)
    result = []
    count = 0
    for m in model.metrics_names:
        if count > 0:
            result.append({"metric": m, "score": scores[count]})
        count = count + 1;
    
    # serialize model to JSON
    model_json = model.to_json()
    with open(modelFolder + "/model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(modelFolder + "/model.hdf5")
    keras.utils.plot_model(model, to_file=modelFolder + '/model.png', show_layer_names=True, show_shapes=True)
    return result

def ContinueTraining(modelDef, trainFile, modelFolder, epoch=0, batch_size=0):
    json_file = open(modelFolder + '/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(modelFolder + "/model.hdf5")
    model.compile(loss=modelDef['trainingparam']['loss'], optimizer=modelDef['trainingparam']['optimizer'], metrics=modelDef['scoring'])
    if modelDef['dataset']['column_header'] == True:
        dataframe = read_csv(trainFile, delim_whitespace=modelDef['dataset']['delim_whitespace'])
    else:
        dataframe = read_csv(trainFile, delim_whitespace=modelDef['dataset']['delim_whitespace'], header=None)
    
    if modelDef['dataset']['colsdefined'] == True:
        X_frame = dataframe[modelDef['xcols']]
        Y_frame = dataframe[modelDef['ycols']]
        X = X_frame.values
        Y = Y_frame.values
    else:
        array = dataframe.values
        rsplit = modelDef['dataset']['xrange'].split(":")
        X = array[:, int(rsplit[0]):int(rsplit[1])]
        Y = array[:, modelDef['dataset']['yrange']]
    
    X = utility.scaleData(modelDef['preprocessdata'], X)
    seed = 7
    numpy.random.RandomState(seed)
    #numpy.random.seed(seed)
    kfold = KFold(n_splits=10, random_state=seed)
    if epoch == 0:
        epoch = modelDef['trainingparam']['epoches']
    
    if batch_size == 0:
        batch_size = modelDef['trainingparam']['batch_size']
    model.fit(X, Y, epochs=epoch, batch_size=batch_size, verbose=1)
    scores = model.evaluate(X, Y, verbose=0)
    result = []
    count = 0
    for m in model.metrics_names:
        if count > 0:
            result.append({"metric": m, "score": scores[count]})
        count = count + 1;
    
    # serialize model to JSON
    model_json = model.to_json()
    with open(modelFolder + "/model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(modelFolder + "/model.hdf5")

    return result

def Predict(modelDef, modelFolder, testFile):
    json_file = open(modelFolder + '/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(modelFolder + "/model.hdf5")
    if modelDef['dataset']['column_header'] == True:
        dataframe = read_csv(testFile, delim_whitespace=modelDef['dataset']['delim_whitespace'])
    else:
        dataframe = read_csv(testFile, delim_whitespace=modelDef['dataset']['delim_whitespace'], header=None)
    
    if modelDef['dataset']['colsdefined'] == True:
        X_frame = dataframe[modelDef['xcols']]
        Y_frame = dataframe[modelDef['ycols']]
        X = X_frame.values
        Y = Y_frame.values
    else:
        array = dataframe.values
        rsplit = modelDef['dataset']['xrange'].split(":")
        X = array[:, int(rsplit[0]):int(rsplit[1])]
        Y = array[:, modelDef['dataset']['yrange']]
    
    X = utility.scaleData(modelDef['preprocessdata'], X)
    Y = model.Predict(X)
    dataframe['Result'] = Y
    dataframe.to_csv(modelFolder + '/dataset/prediction.csv')
    return Y