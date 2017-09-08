from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from projectmodels import *
import simplejson as json
from datetime import datetime
import uuid

engine = create_engine(DBPath())
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = scoped_session(DBSession)

def GetService(srvname, srvtype):
    result = None
    try:
        result = session.query(Service).filter(Service.servicetype == srvtype).filter(Service.servicename == srvname).one()
    except NoResultFound as e:
        result = None

    return result

def ValidateServiceExists(srvname, srvtype):
    s = GetService(srvname, srvtype)
    if s is None:
        raise Exception("Service does not exists")

def GetServices(srvtype):
    result = None
    try:
        result = session.query(Service).filter(Service.servicetype == srvtype).all()
    except NoResultFound as e:
        result = None

    return result

def GetPipeline(srvname, srvtype):
    result = None
    try:
        result = session.query(Pipeline).filter(Pipeline.servicetype == srvtype).filter(Pipeline.servicename == srvname).one()
    except NoResultFound as e:
        result = None

    return result

def UpsertService(srvname, srvtype, srvdata):
    try:
        srv = GetService(srvname, srvtype)
        if srv is None:
            srv = Service(servicename=srvname, servicetype=srvtype, servicedata=json.dumps(srvdata), createdon=datetime.utcnow(), modifiedon=datetime.utcnow())
            session.add(srv)
        else:
            srv.servicedata = json.dumps(srvdata)
            srv.modifiedon = datetime.utcnow()

        session.commit()
    except:
        session.rollback()
        raise

def UpsertPipeline(srvname, srvtype, pipelinedata):
    try:
        pd = GetPipeline(srvname, srvtype)
        if pd is None:
            pd = Pipeline(servicename=srvname, servicetype=srvtype, pipelinedata=json.dumps(pipelinedata), createdon=datetime.utcnow(), modifiedon=datetime.utcnow())
            session.add(pd)
        else:
            pd.pipelinedata = json.dumps(pipelinedata)
            pd.modifiedon = datetime.utcnow()
        session.commit()
    except:
        session.rollback()
        raise

def DeleteService(srvname, srvtype):
    try:
        srv = GetService(srvname, srvtype)
        session.delete(srv)
        session.commit()
    except:
        session.rollback()
        raise

def DeletePipeline(srvname, srvtype):
    try:
        pd = GetPipeline(srvname, srvtype)
        session.delete(pd)
        session.commit()
    except:
        raise

def GetJob(id):
    result = None
    try:
        result = session.query(TrainingJob).filter(TrainingJob.id == id).one()
    except NoResultFound as e:
        result = None

    return result

def GetJobs(srvname, srvtype):
    result = session.query(TrainingJob).filter(TrainingJob.servicetype == srvtype).filter(TrainingJob.servicename == srvname).all()
    return result

def StartJob(srvname, srvtype, totalepoch):
    try:
        id = str(uuid.uuid4())
        job = TrainingJob(id=id, servicename=srvname, servicetype=srvtype, start=datetime.utcnow(), status="Started", createdon=datetime.utcnow(), totalepoch=totalepoch)
        session.add(job)
        session.commit()
    except:
        session.rollback()
        raise
    return id

def EndJob(id, status, message, result=None):
    try:
        job = GetJob(id)
        job.end = datetime.utcnow()
        job.status = status
        job.message = message
        job.result = result
        session.commit()
    except:
        session.rollback()
        raise

def UpdateModelHistory(id, history):
    try:
        job = GetJob(id)
        job.modelhistory = history
        session.commit()
    except:
        raise

def ClearCurrentTraining(id):
    try:
        session.query(CurrentTraining).filter(CurrentTraining.id == id).delete()
        session.commit()
    except:
        session.rollback()
        raise

def LogCurrentTraining(id, epoch, loss):
    try:
        log = CurrentTraining(id=id, epoch=epoch, loss=loss)
        session.add(log)
        session.commit()
    except:
        session.rollback()
        raise

def GetCurrentTraining(id):
    return session.query(CurrentTraining).filter(CurrentTraining.id == id).order_by(CurrentTraining.epoch).all()