from keras import applications
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, Input
from keras import backend as K
import numpy as np
from Interface import utility

modellist = []

def buildModel(name, target_x, target_y):
    input_tensor = Input(shape=(target_x, target_x, 3))
    if name == "ResNet50":
        model = applications.resnet50.ResNet50(input_tensor=input_tensor)
    elif name == "VGG16":
        model = applications.vgg16.VGG16(input_tensor=input_tensor)
    elif name == "VGG19":
        model = applications.vgg19.VGG19(input_tensor=input_tensor)
    elif name == "InceptionV3":
        model = applications.inception_v3.InceptionV3(input_tensor=input_tensor)
    elif name == "Xception":
        model = applications.xception.Xception(input_tensor=input_tensor)
    
    return model

def processInput(name, x):
    if name == "ResNet50":
        x = applications.resnet50.preprocess_input(x)
    elif name == "VGG16":
        x = applications.vgg16.preprocess_input(x)
    elif name == "VGG19":
        x = applications.vgg19.preprocess_input(x)
    elif name == "InceptionV3":
        x = applications.inception_v3.preprocess_input(x)
    elif name == "Xception":
        x = applications.xception.preprocess_input(x)
    
    return x

def decodePred(name, preds):
    if name == "ResNet50":
        x = applications.resnet50.decode_predictions(preds)
    elif name == "VGG16":
        x = applications.vgg16.decode_predictions(preds)
    elif name == "VGG19":
        x = applications.vgg19.decode_predictions(preds)
    elif name == "InceptionV3":
        x = applications.inception_v3.decode_predictions(preds)
    elif name == "Xception":
        x = applications.xception.decode_predictions(preds)
    
    return x

def predict(modelDef, img_path):
    target_x = modelDef['image']['target_size_x']
    target_y = modelDef['image']['target_size_y']
    name = modelDef['model']
    modelname = modelDef['name']
    foundModel = False
    for m in modellist:
        if m['name'] == name:
            model = m['model']
            foundModel = True
    
    if not foundModel:
        model = buildModel(name, target_x, target_y)
        modellist.append({"name": name, "model": model})
        utility.updateModelResetCache(modelname, False)
    else:
        if modelDef['reset_cache']:
            model = buildModel(name, target_x, target_y)
            for m in modellist:
                if m['name'] == name:
                    m['model'] = model
                    utility.updateModelResetCache(modelname, False)

    img = image.load_img(img_path, target_size=(target_x, target_y))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = processInput(name, x)
    preds = decodePred(name, model.predict(x))
    result = []
    for p in preds[0]:
        result.append({"synset": p[0], "text": p[1], "prediction": float("{0:.2f}".format((p[2] * 100)))})

    return result
