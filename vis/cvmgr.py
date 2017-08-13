import cv2
import sys
import simplejson as json
import jsonpickle
from PIL import Image
import pytesseract
import os
import numpy

face_cascade_xml = "./data/__vision/haarcascades/haarcascade_frontalface_default.xml"
class NumpyFloatHandler(jsonpickle.handlers.BaseHandler):
    """
    Automatic conversion of numpy float  to python floats
    Required for jsonpickle to work correctly
    """
    def flatten(self, obj, data):
        """
        Converts and rounds a Numpy.float* to Python float
        """
        return round(obj,6)

def detectfaces(imgpath):
    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = cv2.CascadeClassifier(face_cascade_xml)
    rects = detector.detectMultiScale(gray, 1.3, 5)
    result = []
    for (x, y, w, h) in rects:
        result.append({"x": x, "y": y, "w": w, "h": h})
    jsonpickle.handlers.registry.register(numpy.int32, NumpyFloatHandler)
    jsonpickle.handlers.registry.register(numpy.float, NumpyFloatHandler)
    jsonpickle.handlers.registry.register(numpy.float32, NumpyFloatHandler)
    jsonpickle.handlers.registry.register(numpy.float64, NumpyFloatHandler)
    return json.loads(jsonpickle.encode(result, unpicklable=False))

def extracttext(imagepath, preprocess):
    image = cv2.imread(imagepath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    text = pytesseract.image_to_string(Image.open(filename))

    os.remove(filename)
    return {"text": text}
    