from Interface import PipelineComponents, utility
import numpy
import json
import pandas
import importlib

if __name__ == '__main__':
    filepath = "./data/housing/dataset/train.csv"
    options = {"params": {"delim_whitespace": False, "column_header": True}}
    data = PipelineComponents.data_loadcsv(filepath, options)
    options = {"params": {"columns": data.columns}}
    data = PipelineComponents.data_filtercolumns(data, options)
    options = {"params": {"xcols": ["crim", "zn", "indus", "chas", "nox", "rm", "age", "dis"], "ycols": ["medv"]}}
    (X,Y) = PipelineComponents.data_getxy(data, options)
    options = {"method": "VarianceThreshold", "transform": True, "params": {"threshold": 0.0}}
    (f, Xframe) = PipelineComponents.data_featureselection(X, Y, options)
    print(f)
    
    