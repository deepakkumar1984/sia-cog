from pandas import read_csv
from pandas import set_option
import matplotlib.pyplot as plt, mpld3
from Interface import plotmgr, utility
import simplejson as json
import jsonpickle

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

def plot(name, filename, method, options=None):
    df = loaddata(name, filename)
    d = []
    if method == "factor":
        utility.validateParam(options, "x")
        utility.validateParam(options, "y")
        d = plotmgr.Axis_FactorPlot(df, options["x"], options["y"], utility.getVal(options, "hue")
                                    , utility.getVal(options, "row"), utility.getVal(options, "col")
                                    , utility.getVal(options, "kind", "point"))
    elif method == "lm":
        utility.validateParam(options, "x")
        utility.validateParam(options, "y")
        d = plotmgr.Axis_LMPlot(df, options["x"], options["y"], utility.getVal(options, "hue"))
    elif method == "pair":
        d = plotmgr.Axis_PairPlot(df, utility.getVal(options, "hue"))
    elif method == "joint":
        utility.validateParam(options, "x")
        utility.validateParam(options, "y")
        d = plotmgr.Axis_JointPlot(df, options["x"], options["y"], utility.getVal(options, "kind", "scatter"))
    elif method == "strip":
        utility.validateParam(options, "x")
        d = plotmgr.Cat_StripPlot(df, options["x"], utility.getVal(options, "y"),
                                utility.getVal(options, "hue"), utility.getVal(options, "jitter", False))
    elif method == "swarm":
        utility.validateParam(options, "x")
        d = plotmgr.Cat_SwarmPlot(df, options["x"], utility.getVal(options, "y"), utility.getVal(options, "hue"))
    elif method == "box":
        utility.validateParam(options, "x")
        d = plotmgr.Cat_BoxPlot(df, options["x"], utility.getVal(options, "y"), utility.getVal(options, "hue"))
    elif method == "violin":
        utility.validateParam(options, "x")
        d = plotmgr.Cat_ViolinPlot(df, options["x"], utility.getVal(options, "y"), utility.getVal(options, "hue"))
    elif method == "lv":
        utility.validateParam(options, "x")
        d = plotmgr.Cat_LVPlot(df, options["x"], utility.getVal(options, "y"), utility.getVal(options, "hue"))
    elif method == "point":
        utility.validateParam(options, "x")
        d = plotmgr.Cat_LVPlot(df, options["x"], utility.getVal(options, "y"), utility.getVal(options, "hue"))
    elif method == "bar":
        utility.validateParam(options, "x")
        d = plotmgr.Cat_BarPlot(df, options["x"], utility.getVal(options, "y"), utility.getVal(options, "hue"))
    elif method == "count":
        utility.validateParam(options, "x")
        d = plotmgr.Cat_CountPlot(df, options["x"], utility.getVal(options, "y"), utility.getVal(options, "hue"))
    elif method == "reg":
        utility.validateParam(options, "x")
        utility.validateParam(options, "y")
        d = plotmgr.Reg_RegPlot(df, options["x"], utility.getVal(options, "y"))
    elif method == "kde":
        utility.validateParam(options, "x")
        utility.validateParam(options, "y")
        d = plotmgr.Reg_RegPlot(df, options["x"], utility.getVal(options, "y"))
    elif method == "rug":
        utility.validateParam(options, "x")
        d = plotmgr.Reg_RugPlot(df, options["x"])
    return d

