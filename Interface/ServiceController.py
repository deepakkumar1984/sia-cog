from SiaWizard import app
from SiaWizard import DataManager
from SiaWizard.dd_client import DD

setting = DataManager.GetSetting()

def GetServiceInfo(name):
    dd = DD(setting.dd_host, setting.dd_port)
    serviceInfo = dd.get_service(name)
    return serviceInfo

def CreateClassifierCsvService(name, description, mllib, type, layers, classes):
    dd = DD(setting.dd_host, setting.dd_port)
    model = {'templates':'../templates/caffe/','repository':'/data/models/' + name}
    parameters_input = {'connector':'csv'}
    parameters_mllib = {'template':'mlp','nclasses':classes,'layers':layers,'activation':'prelu'}
    parameters_output = {}
    dd.put_service(name,model,description,mllib,
               parameters_input,parameters_mllib,parameters_output)
    return serviceInfo
    