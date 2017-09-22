import cv2
import sys
import simplejson as json
import jsonpickle
from PIL import Image
import pytesseract
import os
import numpy
import urllib

face_cascade_xml = "./vis/haarcascades/haarcascade_frontalface_default.xml"

def detectfaces(imgpath):
    if imgpath.startswith('http://') or imgpath.startswith('https://') or imgpath.startswith('ftp://'):
        image = url_to_image(imgpath)
    else:
        image = cv2.imread(imgpath)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detector = cv2.CascadeClassifier(face_cascade_xml)
    rects = detector.detectMultiScale(gray, 1.3, 5)
    result = []
    for (x, y, w, h) in rects:
        result.append({"x": x, "y": y, "w": w, "h": h})
    return json.loads(jsonpickle.encode(result, unpicklable=False))

def extracttext(imgpath, preprocess):
    if imgpath.startswith('http://') or imgpath.startswith('https://') or imgpath.startswith('ftp://'):
        image = url_to_image(imgpath)
    else:
        image = cv2.imread(imgpath)

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


def url_to_image(url):
    resp = urllib.urlopen(url)
    image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image
    