from pandas import read_csv
from pandas import set_option
import matplotlib.pyplot as plt, mpld3
import seaborn as sns; sns.set()
import simplejson as json
import jsonpickle

def Axis_FactorPlot(data, x, y=None, row=None, col=None, hue=None, kind=None):
    sns.set(style="ticks")
    ax = sns.factorplot(x=x, y=y, hue=hue, data=data, kind=kind, row=row, col=col)
    d = mpld3.fig_to_dict(ax.fig)
    return d

def Axis_LMPlot(data, x, y=None, hue=None):
    sns.set(color_codes=True)
    ax = sns.lmplot(x=x, y=y, hue=hue, data=data)
    d = mpld3.fig_to_dict(ax.fig)
    return d

def Axis_PairPlot(data, hue=None):
    g = sns.pairplot(data, hue=hue)
    d = mpld3.fig_to_dict(g.fig)
    return d

def Axis_JointPlot(data, x, y, kind="scatter"):
    sns.set(style="white", color_codes=True)
    g = sns.jointplot(x, y, data, kind)
    d = mpld3.fig_to_dict(g.fig)
    return d


def Cat_StripPlot(data, x, y, hue=None, jitter=False):
    sns.set_style("whitegrid")
    g = sns.stripplot(x, y, data, hue=hue, jitter=jitter)
    d = mpld3.fig_to_dict(g.fig)
    return d

def Cat_SwarmPlot(data, x, y=None, hue=None):
    sns.set_style("whitegrid")
    g = sns.swarmplot(x, y, data, hue=hue)
    d = mpld3.fig_to_dict(g.fig)
    return d

def Cat_BoxPlot(data, x, y=None, hue=None):
    sns.set_style("whitegrid")
    g = sns.boxplot(x, y, data, hue=hue)
    d = mpld3.fig_to_dict(g.fig)
    return d

def Cat_ViolinPlot(data, x, y=None, hue=None):
    sns.set_style("whitegrid")
    g = sns.violinplot(x, y, data, hue=hue)
    d = mpld3.fig_to_dict(g.fig)
    return d

def Cat_LVPlot(data, x, y=None, hue=None):
    sns.set_style("whitegrid")
    g = sns.lvplot(x, y, data, hue=hue)
    d = mpld3.fig_to_dict(g.fig)
    return d

def Cat_PointPlot(data, x, y, hue=None):
    sns.set_style("whitegrid")
    g = sns.pointplot(x, y, data, hue=hue)
    d = mpld3.fig_to_dict(g.fig)
    return d

def Cat_BarPlot(data, x, y, hue=None):
    sns.set_style("whitegrid")
    g = sns.barplot(x, y, data, hue=hue)
    d = mpld3.fig_to_dict(g.fig)
    return d

def Cat_CountPlot(data, x=None, y=None, hue=None):
    sns.set_style("whitegrid")
    g = sns.countplot(x, y, data, hue=hue)
    d = mpld3.fig_to_dict(g.fig)
    return d

