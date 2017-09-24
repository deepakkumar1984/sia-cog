models = {}

def store(srvtype, srvname, model):
    name = srvtype + srvname
    models[name] = model

def get(srvtype, srvname):
    name = srvtype + srvname
    result = None
    if name in models:
        result = models[name]
    return result