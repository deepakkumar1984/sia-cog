import pandas
from pandas import read_csv
import json
from sklearn.preprocessing import Imputer
from sklearn import preprocessing, feature_selection

def data_loadcsv(filename, options):
    if options['params']['column_header'] == True:
        dataframe = read_csv(filename, delim_whitespace=options['params']['delim_whitespace'])
    else:
        dataframe = read_csv(filename, delim_whitespace=options['params']['delim_whitespace'], header=None)

    return dataframe

def data_filtercolumns(dataframe, options):
    cols = options["params"]["columns"]
    dataframe = dataframe[cols]
    
    return dataframe

def data_getxy(dataframe, options):
    X_frame = dataframe[options['params']['xcols']]
    Y_frame = dataframe[options['params']['ycols']]
    
    return (X_frame,Y_frame)

def data_handlemissing(dataframe, options):
    if options['params']['type'] == "dropcolumns":
        thresh = options['params']['thresh']
        if thresh == -1:
            dataframe.dropna(axis=1, how="all", inplace=True)
        elif thresh == 0:
            dataframe.dropna(axis=1, how="any", inplace=True)
        elif thresh > 0:
            dataframe.dropna(axis=1, thresh=thresh, inplace=True)
    elif options['params']['type'] == "droprows":
        thresh = options['params']['thresh']
        if thresh == -1:
            dataframe.dropna(axis=0, how="all", inplace=True)
        elif thresh == 0:
            dataframe.dropna(axis=0, how="any")
        elif thresh > 0:
            dataframe.dropna(axis=0, thresh=thresh)
    elif options['params']['type'] == "fillmissing":
        strategy = options['params']['strategy']
        imp = Imputer(missing_values='NaN', strategy=strategy, axis=0)
        array = imp.fit_transform(dataframe.values)
        return pandas.DataFrame(array, columns = dataframe.columns)

def data_preprocess(dataframe, options):
    method = options['method']
    data = dataframe.values
    module = eval("preprocessing." + method)()
    m = getattr(module, "fit_transform")
    data = m(data)
    return pandas.DataFrame(data, columns = dataframe.columns)

def data_featureselection(Xframe, Yframe, options):
    method = options['method']
    transform = options['transform']
    args = {}
    for p in options["params"]:
        if "score_func" in p:
            scorefunc = eval("feature_selection." + options["params"][p])
            args[p] = scorefunc
            continue
            
        args[p] = options["params"][p]

    module = eval("feature_selection." + method)(**args)
    fit = getattr(module, "fit")
    mtransform = getattr(module, "fit_transform")
    f = fit(Xframe, Yframe)
    names = Xframe.columns
    if transform is True:
        data = mtransform(Xframe, Yframe)
        Xframe = data

    result = {}

    if method == "VarianceThreshold":
        result['variances'] = sorted(zip(map(lambda x: round(x, 4), f.variances_), names), reverse=True)
    else:
        result['scores'] = sorted(zip(map(lambda x: round(x, 4), f.scores_), names), reverse=True)
        result['pvalues'] = sorted(zip(map(lambda x: round(x, 4), f.pvalues_), names), reverse=True)
    return (result, Xframe)


def data_featureselection_withestimator(estimator, Xframe, Yframe, options):
    method = options['method']
    transform = options['transform']
    args = {}
    for p in options["params"]:
        if "score_func" in p:
            scorefunc = eval("feature_selection." + options["params"][p])
            args[p] = scorefunc
            continue

        args[p] = options["params"][p]

    module = eval("feature_selection." + method)(estimator = estimator , **args)
    fit = getattr(module, "fit")
    mtransform = getattr(module, "fit_transform")
    f = fit(Xframe, Yframe)
    names = Xframe.columns
    if transform is True:
        data = mtransform(Xframe, Yframe)
        Xframe = data

    result = {}
    result['scores'] = sorted(zip(map(lambda x: round(x, 4), f.scores_), names), reverse=True)
    result['pvalues'] = sorted(zip(map(lambda x: round(x, 4), f.pvalues_), names), reverse=True)
    return (result, Xframe)
    
