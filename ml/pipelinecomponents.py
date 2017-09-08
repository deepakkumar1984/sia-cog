import json
import os
import pickle
import numpy
import pandas
from keras import datasets
from keras.models import model_from_json
from pandas import read_csv
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import Imputer
from keras.utils import np_utils
from ml import scikitlearn, deeplearning

projectfolder = ""
model_type = ""
name = ""
optionslist = {}
jobid = ""

def init(self, name, modeltype, jobid):
    self.projectfolder = "./data/" + name
    self.name = name
    self.jobid = jobid
    self.model_type = modeltype

def addOption(options):
    for op in options:
        optionslist[op] = options[op]

def data_loadcsv(filename, pipeline):
    filename = projectfolder + "/dataset/" + filename
    if pipeline['options']['column_header'] == True:
        dataframe = read_csv(filename, delim_whitespace=pipeline['options']['delim_whitespace'], dtype={'a': numpy.float32})
    else:
        dataframe = read_csv(filename, delim_whitespace=pipeline['options']['delim_whitespace'], header=None, dtype={'a': numpy.float32})

    return dataframe

def data_loadsample(pipeline):
    dataset_name = pipeline["options"]["dataset_name"]
    if dataset_name == "cifar10":
        (X_train, Y_train), (X_test, Y_test) = datasets.cifar10.load_data()
    elif dataset_name == "cifar100":
        (X_train, Y_train), (X_test, Y_test) = datasets.cifar100.load_data()
    elif dataset_name == "imdb":
        (X_train, Y_train), (X_test, Y_test) = datasets.imdb.load_data(path="imdb.npz",
                                                      num_words=None,
                                                      skip_top=0,
                                                      maxlen=None,
                                                      seed=113,
                                                      start_char=1,
                                                      oov_char=2,
                                                      index_from=3)
    elif dataset_name == "reuters":
        (X_train, Y_train), (X_test, Y_test) = datasets.reuters.load_data(path="reuters.npz",
                                                         num_words=None,
                                                         skip_top=0,
                                                         maxlen=None,
                                                         test_split=0.2,
                                                         seed=113,
                                                         start_char=1,
                                                         oov_char=2,
                                                         index_from=3)
    elif dataset_name == "mnist":
        (X_train, Y_train), (X_test, Y_test) = datasets.mnist.load_data()
    elif dataset_name == "boston_housing":
        (X_train, Y_train), (X_test, Y_test) = datasets.boston_housing.load_data()

    return (X_train, Y_train), (X_test, Y_test)

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
    method = pipeline['options']['method']
    data = dataframe.values
    module = eval("preprocessing." + method)()
    m = getattr(module, "fit_transform")
    data = m(data)
    return pandas.DataFrame(data, columns = dataframe.columns)

def image_preprocess(X, Y, pipeline):
    normalize = pipeline["options"]["normalize"]
    encode = pipeline["options"]["encode"]
    reshape = False
    if "reshape" in pipeline["options"]:
        reshape = True
        pixels = pipeline["options"]["reshape"]["pixels"]
        width = pipeline["options"]["reshape"]["width"]
        height = pipeline["options"]["reshape"]["height"]


    if reshape is True:
        X = X.reshape(X.shape[0], pixels, width, height).astype('float32')
    else:
        X = X.astype('float32')

    if normalize is True:
        X = X/255

    if encode is True:
        Y = np_utils.to_categorical(Y)

    num_classes = Y.shape[1]

    return X,Y,num_classes

def data_featureselection(X, Y, pipeline):
    method = pipeline["options"]['method']
    transform = pipeline["options"]['transform']
    args = {}
    for p in pipeline["options"]:
        if "method" in p:
            continue
        if "transform" in p:
            continue

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
        selected_columns = []
        fcount = 0
        for fs in f.get_support():
            if fs == True:
                selected_columns.append(names[fcount])
                fcount = fcount + 1
        X = pandas.DataFrame(data, columns=selected_columns)
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
    method = pipeline["options"]['method']
    transform = pipeline["options"]['transform']
    result = json.loads(result)
    names = result["features"]
    if transform is True:
        X = X[names]

    return X, Y, result

def data_featureselection_withestimator(estimator, X, Y, pipeline):
    method = pipeline["options"]['method']
    transform = pipeline["options"]['transform']
    args = {}
    for p in pipeline["options"]:
        if "method" in p:
            continue
        if "transform" in p:
            continue

        args[p] = pipeline["options"][p]

    module = eval("feature_selection." + method)(estimator = estimator, **args)
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

    result["features"] = selected_columns
    return (X, Y, result)

def model_build(pipeline):
    if model_type == "mlp":
        model = deeplearning.buildModel(pipeline)
    else:
        model = scikitlearn.getSKLearnModel(pipeline['options']['method'])
    return model

def model_evaluate(model, X, Y, pipeline):
    if "scoring" in pipeline["options"]:
        if len(pipeline['options']['scoring']) > 0:
            scoring = pipeline['options']['scoring']
        else:
            scoring = "neg_mean_squared_error"
    else:
        scoring = "neg_mean_squared_error"

    kfold = 10
    if "kfold" in pipeline['options']:
        kfold = pipeline["options"]["kfold"]

    results = cross_validate(model, X, Y, cv=kfold, scoring=scoring)
    output = {"mean": results.mean(), "std": results.std(), "results": results}
    model.fit(X, Y)
    picklefile = projectfolder + "/model.out"
    with open(picklefile, "wb") as f:
        pickle.dump(model, f)

    return output

def model_train(model, X, Y, pipeline, more = False):
    if model_type == "mlp":
        modelObj = model_from_json(model)
        modelObj.compile(loss=pipeline['options']['loss'], optimizer=pipeline['options']['optimizer'],
                      metrics=pipeline['options']['scoring'])
        epoches = pipeline["options"]["epoches"]
        batch_size = pipeline["options"]["batch_size"]
        weightpath = projectfolder + "/weights.hdf5"
        if more == "true":
            if os.path.exists(weightpath):
                modelObj.load_weights(weightpath)
        deeplearning.init(deeplearning, name, jobid)
        result = deeplearning.Train(modelObj, X, Y, weightpath, epoches, batch_size)
        picklefile = projectfolder + "/model.json"
        model_json = modelObj.to_json()
        with open(picklefile, "w") as json_file:
            json_file.write(model_json)

    return result

def model_predict(X, pipeline):
    if model_type == "mlp":
        json_file = open(projectfolder + '/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights(projectfolder + "/weights.hdf5")
        model.compile(loss=pipeline['options']['loss'], optimizer=pipeline['options']['optimizer'],
                         metrics=pipeline['options']['scoring'])
        if type(X) is pandas.DataFrame:
            X = X.values
        Y = model.predict(X)
    else:
        picklefile = projectfolder + "/model.out"
        with open(picklefile, "rb") as f:
            model = pickle.load(f)
        Y = model.predict(X)

    return Y

def return_result(outputname, num = None):
    pickleFile = projectfolder + '/pipeline.out'
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

