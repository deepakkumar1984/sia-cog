from pandas import read_csv
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold 
from sklearn.model_selection import cross_val_score 
from sklearn import datasets, linear_model
from keras.wrappers.scikit_learn import KerasRegressor

def Run(modelDef, filename):
    dataframe = read_csv(filename)
    array = dataframe.values
    
    X = array[:,0:13]
    Y = array[:,13]
    num_folds = 10
    kfold = KFold(n_splits=10, random_state=7)
    model = linear_model.LinearRegression()
    scoring = 'neg_mean_squared_error'
    results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    print("MSE: %.3f (%.3f)") % (results.mean(), results.std())



