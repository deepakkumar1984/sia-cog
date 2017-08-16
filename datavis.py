
import json
import jsonpickle
from Interface import dataanalyzer

d = dataanalyzer.basic_info("housing", "train.csv")
print(json.loads(d))
#iris = sns.load_dataset("iris")
#g = sns.PairGrid(iris)

#g = g.map(plt.scatter)
#plt.show()
#plt.savefig("test.jpg")
#d = mpld3.fig_to_dict(g.fig)

#str = json.dumps(d)
#print(str)
