import pandas
from pandas import read_csv
import json
from sklearn import preprocessing, feature_selection, feature_extraction, decomposition
from sklearn.preprocessing import Imputer
from sklearn.model_selection import cross_val_score
import pickle
import os
from sklearn.model_selection import KFold
from Interface import SkLearnTask

projectfolder = ""

def init(self, name):
    self.projectfolder = "./data/" + name

def data_loadcsv(filename, pipeline):
    filename = projectfolder + "/dataset/" + filename
    if pipeline['options']['column_header'] == True:
        dataframe = read_csv(filename, delim_whitespace=pipeline['options']['delim_whitespace'])
    else:
        dataframe = read_csv(filename, delim_whitespace=pipeline['options']['delim_whitespace'], header=None)

    return dataframe

def data_filtercolumns(dataframe, pipeline):
    cols = pipeline["options"]["columns"]
    dataframe = dataframe[cols]

    return dataframe

def data_getxy(dataframe, pipeline):
    X_frame = dataframe[pipeline['options']['xcols']]
    Y_frame = dataframe[pipeline['options']['ycols']]
    
    return (X_frame,Y_frame)


def data_getx(dataframe, pipeline):
    X_frame = dataframe[pipeline['options']['xcols']]

    return (X_frame, 0)

def data_handlemissing(dataframe, pipeline):
    if pipeline['options']['type'] == "dropcolumns":
        thresh = pipeline['options']['thresh']
        if thresh == -1:
            dataframe.dropna(axis=1, how="all", inplace=True)
        elif thresh == 0:
            dataframe.dropna(axis=1, how="any", inplace=True)
        elif thresh > 0:
            dataframe.dropna(axis=1, thresh=thresh, inplace=True)
    elif pipeline['options']['type'] == "droprows":
        thresh = pipeline['options']['thresh']
        if thresh == -1:
            dataframe.dropna(axis=0, how="all", inplace=True)
        elif thresh == 0:
            dataframe.dropna(axis=0, how="any", inplace=True)
        elif thresh > 0:
            dataframe.dropna(axis=0, thresh=thresh)
    elif pipeline['options']['type'] == "fillmissing":
        strategy = pipeline['options']['strategy']
        imp = Imputer(missing_values='NaN', strategy=strategy, axis=0)
        array = imp.fit_transform(dataframe.values)
        dataframe = pandas.DataFrame(array, columns = dataframe.columns)

    return dataframe

def data_preprocess(dataframe, pipeline):
    method = pipeline['method']
    data = dataframe.values
    module = eval("preprocessing." + method)()
    m = getattr(module, "fit_transform")
    data = m(data)
    return pandas.DataFrame(data, columns = dataframe.columns)

def data_featureselection(X, Y, pipeline):
    method = pipeline['method']
    transform = pipeline['transform']
    args = {}
    for p in pipeline["options"]:
        if "score_func" in p:
            scorefunc = eval("feature_selection." + pipeline["options"][p])
            args[p] = scorefunc
            continue
            
        args[p] = pipeline["options"][p]

    module = eval("feature_selection." + method)(**args)
    fit = getattr(module, "fit")
    mtransform = getattr(module, "fit_transform")
    f = fit(X.values, Y.values)
    names = X.columns
    result = {}

    if transform is True:
        data = mtransform(X.values, Y.values)
        X = data
        selected_columns = []
        fcount = 0
        for fs in f.get_support():
            if fs == True:
                selected_columns.append(names[fcount])
                fcount = fcount + 1
    else:
        selected_columns = names

    if method == "VarianceThreshold":
        result['variances'] = sorted(zip(map(lambda x: round(x, 4), f.variances_), names), reverse=True)
    else:
        result['scores'] = sorted(zip(map(lambda x: round(x, 4), f.scores_), names), reverse=True)
        result['pvalues'] = sorted(zip(map(lambda x: round(x, 4), f.pvalues_), names), reverse=True)

    result["features"] = selected_columns
    return X, Y, result


def data_getfeatures(X, Y, result, pipeline):
    method = pipeline['method']
    transform = pipeline['transform']
    names = result["features"]
    result = {}

    if transform is True:
        X = X[names]

    return X

def data_featureselection_withestimator(estimator, X, Y, pipeline):
    method = pipeline['method']
    transform = pipeline['transform']
    args = {}
    for p in pipeline["options"]:
        if "score_func" in p:
            scorefunc = eval("feature_selection." + pipeline["options"][p])
            args[p] = scorefunc
            continue

        args[p] = pipeline["options"][p]

    module = eval("feature_selection." + method)(estimator = estimator , **args)
    fit = getattr(module, "fit")
    mtransform = getattr(module, "fit_transform")
    f = fit(X, Y)
    names = X.columns
    if transform is True:
        data = mtransform(X, Y)
        X = data
        selected_columns = []
        fcount = 0
        for fs in f.get_support():
            if fs == True:
                selected_columns.append(names[fcount])
                fcount = fcount + 1
    else:
        selected_columns = names

    result = {}
    result['scores'] = sorted(zip(map(lambda x: round(x, 4), f.scores_), names), reverse=True)
    result['pvalues'] = sorted(zip(map(lambda x: round(x, 4), f.pvalues_), names), reverse=True)
    result["features"] = selected_columns
    return (X, Y, result)

def model_build(pipeline):
    model = SkLearnTask.getSKLearnModel(pipeline['method'])
    return model

def model_crossvalidate(model, X, Y, pipeline):
    if "scoring" in pipeline["options"]:
        if len(pipeline['options']['scoring']) > 0:
            scoring = pipeline['options']['scoring'][0]
        else:
            scoring = "neg_mean_squared_error"
    else:
        scoring = "neg_mean_squared_error"

    kfold = 10
    if "kfold" in pipeline['options']:
        kfold = pipeline["options"]["kfold"]

    results = cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
    output = {"mean": results.mean(), "std": results.std(), "results": results}
    return output

def model_fit(model, X, Y, pipeline):
    model.fit(X, Y)
    picklefile = projectfolder + "/model.out"
    with open(picklefile, "wb") as f:
        pickle.dump(model, f)
    return model

def model_predict(X, pipeline):
    picklefile = projectfolder + "/model.out"
    with open(picklefile, "rb") as f:
        model = pickle.load(f)

    Y = model.predict(X)
    return Y

def readOutput(srvname, outputname, num = None):
    pickleFile = './data/' + srvname + '/pipeline.out'
    with open(pickleFile, 'rb') as f:
        resultset = pickle.load(f)

    result = None
    if num is None:
        outputname = "output->" + outputname
    else:
        outputname = "output->" + outputname + "->" + str(num)

    count = 0
    resultDict = {}
    for r in resultset:
        if outputname in r:
            if count > 0:
                resultDict[count - 1] = result
                resultDict[count] = resultset[r]
            else:
                result = resultset[r]

            count = count+1

    if count > 1:
        return resultDict

    return result

