from Interface import PipelineComponents, utility
import numpy
import json
import pandas
import importlib

if __name__ == '__main__':
    filepath = "./data/housing/pipeline.json"    
    resultSet = {}
    pipelineJson = json.loads(utility.getFileData(filepath))
    