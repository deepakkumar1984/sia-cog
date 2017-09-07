from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from projectmodels import *
import simplejson as json
from datetime import datetime
import uuid

engine = create_engine(DBPath())
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def GetService(srvname, srvtype):
    result = None
    try:
        result = session.query(Service).filter(Service.servicetype == srvtype).filter(Service.servicename == srvname).one()
    except NoResultFound as e:
        result = None

    return result

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
    srv = GetService(srvname, srvtype)
    if srv is None:
        srv = Service(servicename=srvname, servicetype=srvtype, servicedata=json.dumps(srvdata), createdon=datetime.utcnow(), modifiedon=datetime.utcnow())
        session.add(srv)
        session.commit()
    else:
        srv.servicedata = json.dumps(srvdata)
        srv.modifiedon = datetime.utcnow()
        session.commit()

def UpsertPipeline(srvname, srvtype, pipelinedata):
    pd = GetPipeline(srvname, srvtype)
    if pd is None:
        pd = Pipeline(servicename=srvname, servicetype=srvtype, pipelinedata=json.dumps(pipelinedata), createdon=datetime.utcnow(), modifiedon=datetime.utcnow())
        session.add(pd)
        session.commit()
    else:
        pd.pipelinedata = json.dumps(pipelinedata)
        pd.modifiedon = datetime.utcnow()
        session.commit()

def DeleteService(srvname, srvtype):
    srv = GetService(srvname, srvtype)
    session.delete(srv)
    session.commit()

def DeletePipeline(srvname, srvtype):
    pd = GetPipeline(srvname, srvtype)
    session.delete(pd)
    session.commit()

def GetJob(id):
    result = None
    try:
        result = session.query(TrainingJob).filter(TrainingJob.id == id).one()
    except NoResultFound as e:
        result = None

    return result

def StartJob(srvname, srvtype, totalepoch):
    id = str(uuid.uuid4())
    job = TrainingJob(id=id, servicename=srvname, servicetype=srvtype, start=datetime.utcnow(), status="Started", createdon=datetime.utcnow(), totalepoch=totalepoch)
    session.add(job)
    session.commit()

def EndJob(id, status, message, result=None, learninghistory=None):
    job = GetJob(id)
    job.end = datetime.utcnow()
    job.status = status
    job.message = message
    job.result = result
    job.learninghistory = learninghistory
    session.commit()



