from sqlalchemy.orm import sessionmaker
from logmodels import *
from sqlalchemy.orm import scoped_session
from datetime import datetime, timedelta
from sqlalchemy import func

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
    result = session.query(PredLog).filter(PredLog.servicetype == srvtype).filter(PredLog.servicename == srvname).filter(PredLog.createdon >= fromdate).filter(PredLog.createdon <= todate).filter(PredLog.status == status.upper()).all()
    return result

def GetTopCalls():
    lastdate = datetime.utcnow() + timedelta(days=-14)
    result = session.query(func.count(PredLog.servicename).label("count"), PredLog.servicename, PredLog.servicetype).filter(PredLog.createdon >= lastdate).group_by(PredLog.servicename, PredLog.servicetype).order_by(func.count(PredLog.servicename).desc()).all();
    return result

def GetTopErrors():
    lastdate = datetime.utcnow() + timedelta(days=-14)
    result = session.query(func.count(PredLog.servicename).label("count"), PredLog.servicename, PredLog.servicetype).filter(PredLog.status == "ERROR").filter(PredLog.createdon >= lastdate).group_by(PredLog.servicename, PredLog.servicetype).order_by(func.count(PredLog.servicename).desc()).all();
    return result