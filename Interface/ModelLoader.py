from keras.models import Sequential, model_from_json
import keras

loadedList = []

def load(name):
    for m in loadedList:
        if m['name'] == name:
            model = m['model']
    
    return model
