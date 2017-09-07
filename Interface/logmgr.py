from sqlalchemy.orm import sessionmaker
from logmodels import *
from datetime import datetime

engine = create_engine(DBPath())
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def LogPredSuccess(srvname, srvtype, start):
    end = datetime.utcnow()
    d = end - start
    duration = d.total_seconds()
    log = PredLog(servicename=srvname, servicetype=srvtype, start=start, end=end, duration=duration, status="SUCCESS", createdon=datetime.utcnow())
    session.add(log)
    session.commit()

def LogPredError(srvname, srvtype, start, errormsg):
    end = datetime.utcnow()
    d = end - start
    duration = d.total_seconds()
    log = PredLog(servicename=srvname, servicetype=srvtype, start=start, end=end, duration=duration, message=errormsg, status="ERROR",
                  createdon=datetime.utcnow())
    session.add(log)
    session.commit()