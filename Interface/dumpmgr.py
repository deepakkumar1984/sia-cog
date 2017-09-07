from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from dumpmodel import *
from datetime import datetime

def DumpResult(id, srvname, pipeline, result):
    with create_engine(DBPath(srvname)) as engine:
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        pd = PipelineDump(id=id, pipeline=pipeline, result=result, createdon=datetime.utcnow())
        session.add(pd)
        session.commit()

def GetDump(id, srvname):
    result = None
    try:
        with create_engine(DBPath(srvname)) as engine:
            Base.metadata.bind = engine

            DBSession = sessionmaker(bind=engine)
            session = DBSession()
            result = session.query(PipelineDump).filter(PipelineDump.id == id).one()
    except NoResultFound as e:
        result = None

    return result
