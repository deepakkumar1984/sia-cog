from pandas import read_csv
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold 
from sklearn.model_selection import cross_val_score 
from sklearn import datasets, linear_model
from keras.wrappers.scikit_learn import KerasRegressor

def Run(modelDef, filename):
    dataframe = read_csv(filename)
    print(modelDef['x'])
    X_frame = dataframe[modelDef['x']]
    Y_frame = dataframe[modelDef['y']]
    
    X = X_frame.values
    Y = Y_frame.values
    num_folds = 10
    kfold = KFold(n_splits=10, random_state=7)
    model = linear_model.LinearRegression()
    scoring = ""
    if modelDef.scoring.length > 0:
        scoring = modelDef.scoring[0]
        
    results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    output = {"mean": results.mean(), "std": results.std()}
    return output




