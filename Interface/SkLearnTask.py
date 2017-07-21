from pandas import read_csv
import matplotlib.pyplot as plt
from Interface import utility
from sklearn.model_selection import KFold 
from sklearn.model_selection import cross_val_score 
from sklearn import datasets, linear_model
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn import preprocessing

def getRegressionModel(modelName):
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

def getClassificationModel(modelName):
    if modelName=='MLPClassifier':
        model = MLPClassifier()
    elif modelName=='KNeighborsClassifier':
        model = KNeighborsClassifier()
    elif modelName=='SVC':
        model = SVC()
    elif modelName=='GaussianProcessClassifier':
        model = GaussianProcessClassifier()
    elif modelName=='DecisionTreeClassifier':
        model = DecisionTreeClassifier()
    elif modelName=='RandomForestClassifier':
        model = RandomForestClassifier()
    elif modelName=='AdaBoostClassifier':
        model = AdaBoostClassifier()
    elif modelName=='GaussianNB':
        model = GaussianNB()
    elif modelName=='LogisticRegression':
        model = linear_model.LogisticRegression()
    elif modelName=='QuadraticDiscriminantAnalysis':
        model = QuadraticDiscriminantAnalysis()
    
    return model

def buildModel(modelDef, isregression, filename, fit, X, Y):
    num_folds = 10
    kfold = KFold(n_splits=10, random_state=7)
    if isregression == True:
        model = getRegressionModel(modelDef['model'])
    else:
        model = getClassificationModel(modelDef['model'])
    
    if fit == True:
        model.fit(X, Y)
    
    return model

def Evalute(modelDef, isregression, filename):
    if modelDef['csv']['column_header'] == True:
        dataframe = read_csv(filename, delim_whitespace=modelDef['csv']['delim_whitespace'])
    else:
        dataframe = read_csv(filename, delim_whitespace=modelDef['csv']['delim_whitespace'], header=None)
    
    if modelDef['csv']['colsdefined'] == True:
        X_frame = dataframe[modelDef['xcols']]
        Y_frame = dataframe[modelDef['ycols']]
        X = X_frame.values
        Y = Y_frame.values
    else:
        array = dataframe.values
        rsplit = modelDef['csv']['xrange'].split(":")
        X = array[:, int(rsplit[0]):int(rsplit[1])]
        Y = array[:, modelDef['csv']['yrange']]
    
    X = utility.scaleData(modelDef['preprocessdata'], X)
    model = buildModel(modelDef, isregression, filename, False, X, Y)
    scoring = ""
    if len(modelDef['scoring']) > 0:
        scoring = modelDef['scoring'][0]
    kfold = 10
    results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    output = {"mean": results.mean(), "std": results.std()}
    return output

def Predict(modelDef, isregression, train, test, predictionFile):
    if modelDef['csv']['column_header'] == True:
        dataframe = read_csv(train, delim_whitespace=modelDef['csv']['delim_whitespace'])
    else:
        dataframe = read_csv(train, delim_whitespace=modelDef['csv']['delim_whitespace'], header=None)

    if modelDef['csv']['colsdefined'] == True:
        X_frame = dataframe[modelDef['xcols']]
        Y_frame = dataframe[modelDef['ycols']]
        X = X_frame.values
        Y = Y_frame.values
    else:
        array = dataframe.values
        rsplit = modelDef['csv']['xrange'].split(":")
        X = array[:, int(rsplit[0]):int(rsplit[1])]
        Y = array[:, modelDef['csv']['yrange']]
    
    X = utility.scaleData(modelDef['preprocessdata'], X)
    model = buildModel(modelDef, isregression, train, True, X, Y)
    if modelDef['csv']['column_header'] == True:
        dataframe_test = read_csv(test, delim_whitespace=modelDef['csv']['delim_whitespace'])
    else:
        dataframe_test = read_csv(test, delim_whitespace=modelDef['csv']['delim_whitespace'], header=None)
    
    if modelDef['csv']['colsdefined'] == True:
        X_frame_test = dataframe_test[modelDef['xcols']]
        X_test = X_frame_test.values
    else:
        array_test = dataframe_test.values
        rsplit = modelDef['csv']['xrange'].split(":")
        X_test = array[:, int(rsplit[0]):int(rsplit[1])]
    
    X_test = utility.scaleData(modelDef['preprocessdata'], X_test)
    Y_test = model.predict(X_test)
    dataframe_test['Output'] = Y_test
    
    if modelDef['csv']['colsdefined'] == True:
        dataframe_test.to_csv(predictionFile, index=False, header=False)
    else:
        dataframe_test.to_csv(predictionFile, index=False)

    return Y_test




