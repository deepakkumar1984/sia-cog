from pandas import read_csv
from pandas import set_option
from matplotlib import pyplot
from pandas.tools.plotting import scatter_matrix

def loadData(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    data = read_csv(filename)
    return data

def basicInfo(id):
    data = loadData(id)
    h = data.head()
    html = h.to_html(header=False,border=1)
    filename = "./SiaWizard/static/projects/{}/head.html".format(id)
    result = {"shape": data.shape, "types": data.dtypes}
    with open(filename, 'w') as file:
        file.write(html)

    return result

def dataStats(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    data = read_csv(filename)
    set_option('display.width', 200)
    set_option('precision', 3)
    desc = data.describe();
    html = desc.to_html()
    filename = "./SiaWizard/static/projects/{}/stats.html".format(id)
    with open(filename, 'w') as file:
        file.write(html)

def dataAttrCorrelation(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    data = read_csv(filename)
    correlations = data.corr(method='pearson')
    html = correlations.to_html()
    filename = "./SiaWizard/static/projects/{}/attrcor.html".format(id)
    with open(filename, 'w') as file:
        file.write(html)

def univariantDist(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    data = read_csv(filename)
    skew = data.skew()
    html = skew.to_html()
    filename = "./SiaWizard/static/projects/{}/attrcor.html".format(id)
    with open(filename, 'w') as file:
        file.write(html)

def histPlot(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    savefile = "./SiaWizard/static/projects/{}/hist.png".format(id)
    data = read_csv(filename)
    data.hist()
    pyplot.savefig(savefile);

def densityPlot(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    savefile = "./SiaWizard/static/projects/{}/density.png".format(id)
    data = read_csv(filename)
    data.plot(kind='density', subplots=True, layout=(3,3), sharex=False)
    pyplot.savefig(savefile);

def boxwhiskerPlot(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    savefile = "./SiaWizard/static/projects/{}/bw.png".format(id)
    data = read_csv(filename)
    data.plot(kind='box', subplots=True, layout=(3,3), sharex=False, sharey=False)
    pyplot.savefig(savefile);

def matrixPlot(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    savefile = "./SiaWizard/static/projects/{}/matrix.png".format(id)
    data = read_csv(filename)
    correlations = data.corr()
    # plot correlation matrix
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(correlations, vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = numpy.arange(0,9,1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(names)
    ax.set_yticklabels(names)
    pyplot.savefig(savefile);

def scatterPlot(id):
    filename = "./SiaWizard/static/projects/{}/data.csv".format(id)
    savefile = "./SiaWizard/static/projects/{}/scatter.png".format(id)
    data = read_csv(filename)
    scatter_matrix(data)
    pyplot.savefig(savefile);
