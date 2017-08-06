from vis import cvmgr
import simplejson as json

imgpath = "/home/deepak/work/ml-api/data/__vision/demo/people.jpg"
print(cvmgr.detectfaces(imgpath))

imgpath = "/home/deepak/work/ml-api/data/__vision/demo/ocr.jpg"
print(cvmgr.extracttext(imgpath, "blur"))