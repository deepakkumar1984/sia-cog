from pandas import read_csv
import os
import json

def peek(filepath, count):
    result = []
    data = read_csv(filepath)
    result = data.head(count)
    return result.to_json()

def describe(filepath):
    result = []
    data = read_csv(filepath)
    result = data.describe()
    return result.to_json()

def invoke(name, rjson):
    datasetFolder = "./data/" + name + "/dataset/"
    action = rjson['action']
    filename = rjson['filename']
    filepath = datasetFolder + filename
    if action == 'peek':
        count = 5
        if 'peekcount' in rjson:
            count = rjson['peekcount']
        result = peek(filepath, count)
    elif action == 'describe':
        result = describe(filepath)
    
    return result