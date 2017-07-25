from Interface import PipelineComponents, utility
import numpy
import json
import pandas
import importlib

if __name__ == '__main__':
    filepath = "./data/housing/pipeline.json"    
    resultSet = {}
    pipelineJson = json.loads(utility.getFileData(filepath))
    for p in pipelineJson:
        modulename = p['module']
        if "output->" in modulename:
            module = resultSet[modulename]
        else:
            module = eval(modulename)

        method = p['method']
        if method == "[]":
            result = module[p['params']]
        else:
            m = getattr(module, method)
            if "params" in p:
                args = {}
                for a in p['params']:
                    if "output->" in a:
                        args[a] = resultSet[a]
                    else:
                        args[a] = p['params'][a]

                result = m(**args)
            else:
                result = m()

        resultSet["output->" + p['name']] = result
    
    print(result)
    