from pandas import read_csv
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold 
from sklearn.model_selection import cross_val_score 
from sklearn import datasets, linear_model
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.svm import SVR

def getNormalModel(modelName):
    if modelName=='LinearRegression':
        model = linear_model.LinearRegression()
    elif modelName=='BayesianRidge':
        model = linear_model.BayesianRidge()
    elif modelName=='ARDRegression':
        model = linear_model.ARDRegression()
    elif modelName=='ElasticNet':
        model = linear_model.ElasticNet()
    elif modelName=='HuberRegressor':
        model = linear_model.HuberRegressor()
    elif modelName=='Lasso':
        model = linear_model.Lasso()
    elif modelName=='LassoLars':
        model = linear_model.LassoLars()
    elif modelName=='Rigid':
        model = linear_model.Ridge()
    elif modelName=='SGDRegressor':
        model = linear_model.SGDRegressor()
    elif modelName=='SVR':
        model = SVR()
    
    return model

def buildModel(modelDef, filename, fit):
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
        X = array[:, 0:13]
        Y = array[:, modelDef['dataset']['yrange']]
    
    num_folds = 10
    kfold = KFold(n_splits=10, random_state=7)
    model = getNormalModel(modelDef['model'])
    if fit == True:
        model.fit(X, Y)
    
    return model

def CompileAndValidate(modelDef, filename):
    model = buildModel(modelDef, filename, False)
    scoring = ""
    if len(modelDef['scoring']) > 0:
        scoring = modelDef['scoring'][0]
    
    results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    
    output = {"mean": results.mean(), "std": results.std()}
    return output

def FitAndPredict(modelDef, train, test, savePrediction, predictionFile):
    model = buildModel(modelDef, train, True)
    if modelDef['dataset']['column_header'] == True:
        dataframe_test = read_csv(test, delim_whitespace=modelDef['dataset']['delim_whitespace'])
    else:
        dataframe_test = read_csv(test, delim_whitespace=modelDef['dataset']['delim_whitespace'], header=None)
    
    if modelDef['dataset']['colsdefined'] == True:
        X_frame_test = dataframe_test[modelDef['xcols']]
        X_test = X_frame_test.values
    else:
        array_test = dataframe_test.values
        X_test = array_test[:, 0:13]
    
    Y_test = model.predict(X_test)
    dataframe_test['Output'] = Y_test
    
    if savePrediction == True:
        if modelDef['dataset']['colsdefined'] == True:
            dataframe_test.to_csv(predictionFile, index=False, header=False)
        else:
            dataframe_test.to_csv(predictionFile, index=False)

    return Y_test




