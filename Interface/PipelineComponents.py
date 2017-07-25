import pandas
from pandas import read_csv
import json

def loadcsv(input, options):
    filename = input
    if options['params']['column_header'] == True:
        dataframe = read_csv(filename, delim_whitespace=options['params']['delim_whitespace'])
    else:
        dataframe = read_csv(filename, delim_whitespace=options['params']['delim_whitespace'], header=None)
    
    if options['params']['colsdefined'] == True:
        X_frame = dataframe[options['params']['xcols']]
        Y_frame = dataframe[options['params']['ycols']]
        X = X_frame.values
        Y = Y_frame.values
    else:
        array = dataframe.values
        rsplit = options['params']['xrange'].split(":")
        X = array[:, int(rsplit[0]):int(rsplit[1])]
        Y = array[:, options['params']['yrange']]
    
    return (X,Y)