import json

from Interface import utility
from vis import objcls


def predicttest(name, imgpath):
    directory = "./data/" + name
    modelfile = directory + "/define.json"
    srvfile = directory + "/service.json"
    srvdata = utility.getFileData(srvfile)
    modeldata = utility.getFileData(modelfile)
    modeljson = json.loads(modeldata)
    modeljson['name'] = name
    if modeljson['modeltype'] == 'imagenet':
        result = objcls.predict(modeljson, imgpath)
    
    print(result)

if __name__ == '__main__':
    predicttest('imgcls', './data/imgcls/park.jpg')
    