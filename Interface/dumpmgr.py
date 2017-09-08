from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
import simplejson as json
from dumpmodel import *
from datetime import datetime

def DumpPipelineResult(id, srvname, pipeline, result):
    InitDB(srvname)
    engine = create_engine(DBPath(srvname))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = scoped_session(DBSession)
    try:
        pd = PipelineDump(id=id, pipeline=json.dumps(pipeline), result=result, createdon=datetime.utcnow())
        session.add(pd)
        session.commit()
    except Exception as e:
        session.rollback()
        raise

def DumpMLPResult(id, srvname, mlpjson, result):
    InitDB(srvname)
    engine = create_engine(DBPath(srvname))
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = scoped_session(DBSession)
    try:
        md = MLPDump(id=id, mlpjson=json.dumps(mlpjson), result=result, createdon=datetime.utcnow())
        session.add(md)
        session.commit()
    except Exception as e:
        session.rollback()
        raise

def GetPipelineDump(id, srvname):
    result = None
    try:
        engine = create_engine(DBPath(srvname))
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = scoped_session(DBSession)
        result = session.query(PipelineDump).filter(PipelineDump.id == id).one()
    except NoResultFound as e:
        result = None

    return result

def GetMLPDump(id, srvname):
    result = None
    try:
        engine = create_engine(DBPath(srvname))
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = scoped_session(DBSession)
        result = session.query(MLPDump).filter(MLPDump.id == id).one()
    except NoResultFound as e:
        result = None

    return result
