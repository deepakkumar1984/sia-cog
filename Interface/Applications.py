from keras import applications
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
import numpy as np

def getModel(name):
    if name == "ResNet50":
        model = applications.resnet50.ResNet50()
    elif name == "VGG16":
        model = applications.vgg16.VGG16()
    elif name == "VGG19":
        base_model = applications.vgg19.VGG19()
    elif name == "InceptionV3":
        base_model = applications.inception_v3.InceptionV3()
    elif name == "InceptionV3":
        base_model = applications.inception_v3.InceptionV3()
    elif name == "Xception":
        base_model = applications.xception.Xception()
    
    return model