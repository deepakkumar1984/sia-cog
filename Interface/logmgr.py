from sqlalchemy.orm import sessionmaker
from logmodels import *
from sqlalchemy.orm import scoped_session
from datetime import datetime

engine = create_engine(DBPath())
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)

def LogPredSuccess(srvname, srvtype, start):
    try:
        end = datetime.utcnow()
        d = end - start
        duration = d.total_seconds()
        log = PredLog(servicename=srvname, servicetype=srvtype, start=start, end=end, duration=duration, status="SUCCESS", createdon=datetime.utcnow())
        session.add(log)
        session.commit()
    except:
        session.rollback()
        raise

def LogPredError(srvname, srvtype, start, errormsg):
    try:
        end = datetime.utcnow()
        d = end - start
        duration = d.total_seconds()
        log = PredLog(servicename=srvname, servicetype=srvtype, start=start, end=end, duration=duration, message=errormsg, status="ERROR",
                      createdon=datetime.utcnow())
        session.add(log)
        session.commit()
    except:
        session.rollback()
        raise

def GetLogs(srvname, srvtype, fromdate, todate, status):
    result = session.query(PredLog).filter(PredLog.createdon >= fromdate).filter(PredLog.createdon <= todate).filter(PredLog.status == status.upper()).all()
    return result