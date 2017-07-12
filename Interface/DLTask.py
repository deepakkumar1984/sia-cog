import numpy
from pandas import read_csv
from Interface import utility
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn import preprocessing

def buildModel(modelDef):
    model = Sequential()
    print(modelDef['model'])
    for m in modelDef['model']:
        if m['type'] == 'input':
            model.add(Dense(m['val'], input_dim=m['val'], kernel_initializer=m['init'], activation=m['activation']))   
        elif m['type'] == 'dense':
            model.add(Dense(m['val'], kernel_initializer=m['init'], activation=m['activation']))
        elif m['type'] == 'output':
            model.add(Dense(m['val'], kernel_initializer=m['init']))
    
    model.compile(loss=modelDef['trainingparam']['loss'], optimizer=modelDef['trainingparam']['optimizer'], metrics=modelDef['scoring'])
    return model

def Train(modelDef, isregression, filename, savetofolder):
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
    
    X = utility.scaleData(modelDef['preprocessdata'], X)
    seed = 7
    numpy.random.seed(seed)
    kfold = KFold(n_splits=10, random_state=seed)
    model = buildModel(modelDef)
    print(model)
    model.fit(X, Y, epochs=modelDef['trainingparam']['epoches'], batch_size=modelDef['trainingparam']['batch_size'], verbose=1)
    scores = model.evaluate(X, Y, verbose=0)
    result = []
    count = 0
    for m in model.metrics_names:
        if count > 0:
            result.append({"metric": m, "score": scores[count]})
        count = count + 1;
    
    # serialize model to JSON
    model_json = model.to_json()
    with open(savetofolder + "/model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(savetofolder + "/model.hdf5")

    return result
    
    
    

