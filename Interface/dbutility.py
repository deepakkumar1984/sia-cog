import datetime
from tinydb import TinyDB, Query
from tinydb_serialization import SerializationMiddleware, Serializer

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime.datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')

def getPredLogs(cat, srvname, start, end, success = True):
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
    dbpath = "./data/predlogs_db.json"
    db = TinyDB(dbpath, storage=serialization)
    log = Query()

    return db.search((log.cat == cat)& (log.name == srvname) & (log.success == success) & (log.createdon >= start) & (log.createdon <= end))

def getPredCount(cat, srvname, filterDays = 7):
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
    dbpath = "./data/predlogs_db.json"
    db = TinyDB(dbpath, storage=serialization)
    log = Query()
    filterDate = datetime.datetime.now() - datetime.timedelta(days=filterDays)
    errorCount = db.count((log.cat == cat)& (log.name == srvname) & (log.success == False) & (log.createdon >= filterDate))
    apiCallsCount = db.count((log.cat == cat) & (log.name == srvname) & (log.createdon >= filterDate))
    return apiCallsCount, errorCount

def logCalls(cat, srvname, start, end, success=True, message=""):
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
    dbpath = "./data/predlogs_db.json"
    db = TinyDB(dbpath, storage=serialization)
    d = end - start
    duration = d.total_seconds()
    db.insert({"cat": cat, "name": srvname, "start": start, "end": end, "duration": duration, "success": success, "message": message, "createdon": datetime.datetime.now()})

def logDeepTraining(cat, srvname, epoch, loss, params):
    dbpath = "./data/training_db.json"
    db = TinyDB(dbpath)
    db.insert({"cat": cat, "name": srvname, "epoch": epoch, "loss": loss, "params": params})