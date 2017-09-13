from pandas import read_csv
import matplotlib.pyplot as plt
from Interface import utility
from sklearn.model_selection import KFold 
from sklearn.model_selection import cross_val_score 
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

def getSKLearnModel(modelName):
    if modelName == 'LinearRegression':
        model = linear_model.LinearRegression()
    elif modelName == 'BayesianRidge':
        model = linear_model.BayesianRidge()
    elif modelName == 'ARDRegression':
        model = linear_model.ARDRegression()
    elif modelName == 'ElasticNet':
        model = linear_model.ElasticNet()
    elif modelName == 'HuberRegressor':
        model = linear_model.HuberRegressor()
    elif modelName == 'Lasso':
        model = linear_model.Lasso()
    elif modelName == 'LassoLars':
        model = linear_model.LassoLars()
    elif modelName == 'Rigid':
        model = linear_model.Ridge()
    elif modelName == 'SGDRegressor':
        model = linear_model.SGDRegressor()
    elif modelName == 'SVR':
        model = SVR()
    elif modelName=='MLPClassifier':
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

def getModels():
    result = []
    result.append("LinearRegression")
    result.append("BayesianRidge")
    result.append("ARDRegression")
    result.append("ElasticNet")
    result.append("HuberRegressor")
    result.append("Lasso")
    result.append("LassoLars")
    result.append("Rigid")
    result.append("SGDRegressor")
    result.append("SVR")
    result.append("MLPClassifier")
    result.append("KNeighborsClassifier")
    result.append("SVC")
    result.append("GaussianProcessClassifier")
    result.append("DecisionTreeClassifier")
    result.append("RandomForestClassifier")
    result.append("AdaBoostClassifier")
    result.append("GaussianNB")
    result.append("LogisticRegression")
    result.append("QuadraticDiscriminantAnalysis")
    return result





