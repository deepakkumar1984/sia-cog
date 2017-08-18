import datetime
from tinydb import TinyDB, Query
from tinydb_serialization import SerializationMiddleware, Serializer

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')

def getErrorLogs(srvname, filterDays = 7):
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
    dbpath = "./data/" + srvname + "/logs_db.json"
    db = TinyDB(dbpath, storage=serialization)
    log = Query()
    filterDate = datetime.datetime.now() - datetime.timedelta(days=filterDays)
    return db.search(log.createdon >= filterDate)

def logCalls(srvname, start, end, success=True, message=""):
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
    dbpath = "./data/" + srvname + "/prediction_db.json"
    db = TinyDB(dbpath, storage=serialization)
    d = end - start
    duration = d.total_seconds()
    db.insert({"name": srvname, "start": start, "end": end, "duration": duration, "success": success, "message": message, "createdon": datetime.datetime.now()})