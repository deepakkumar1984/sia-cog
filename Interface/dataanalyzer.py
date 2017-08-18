from pandas import read_csv
from pandas import set_option
import matplotlib.pyplot as plt, mpld3
from Interface import plotmgr
import simplejson as json
import jsonpickle

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

def loaddata(name, filename, columns=None):
    filepath = "./data/" + name + "/dataset/" + filename

    if not columns is None:
        df = read_csv(filepath, columns=columns)
    else:
        df = read_csv(filepath)
        
    return df

def basic_info(name, filename, columns=None, count = 5):
    df = loaddata(name, filename, columns)
    result = {}
    h = df.head(count)
    result["peek"] = h.to_html()
    result["stats"] = df.describe().to_html()
    result["shape"] = df.shape
    result["dtypes"] = json.loads(df.dtypes.to_json())
    result["attr_corr"] = df.corr(method='pearson').to_html()
    result["skew"] = json.loads(df.skew().to_json())

    return jsonpickle.encode(result, unpicklable=False)

def plot(name, filename, method, options=None, x = None, y = None, hue=None):
    df = loaddata(name, filename)
    d = plotmgr.Reg_RegPlot(df, x, y)
    print(d)

