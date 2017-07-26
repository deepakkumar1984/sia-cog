import pandas
from pandas import read_csv
import json
from sklearn.preprocessing import Imputer
from sklearn import preprocessing
from sklearn import feature_selection

def data_loadcsv(filename, options):
    if options['params']['column_header'] == True:
        dataframe = read_csv(filename, delim_whitespace=options['params']['delim_whitespace'])
    else:
        dataframe = read_csv(filename, delim_whitespace=options['params']['delim_whitespace'], header=None)

    return dataframe

def data_filtercolumns(filename, options):
    if options['params']['column_header'] == True:
        dataframe = read_csv(filename, delim_whitespace=options['params']['delim_whitespace'])
    else:
        dataframe = read_csv(filename, delim_whitespace=options['params']['delim_whitespace'], header=None)

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
    name = options['method']
    data = dataframe.values
    m = getattr("preprocessing", name)
    data = m.fit_transform(data)
    return pandas.DataFrame(array, columns = dataframe.columns)

def data_featureselection(Xframe, Yframe, options):
    method = options['method']
    transform = options['transform']
    m = getattr("feature_selection", name)
    m.__init__(options['params']):
    f = m.fit(Xframe.values, Yframe.values)
    if transform:
        data = m.transform(Xframe.values)
    
    Xframe = pandas.DataFrame(data, columns = Xframe.columns)
    return (f, Xframe)
    
