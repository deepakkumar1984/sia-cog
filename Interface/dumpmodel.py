import os
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.types import String, DateTime, Integer

Base = declarative_base()

class PipelineDump(Base):
    __tablename__ = 'pipelinedump'
    id = Column(String, primary_key=True)
    pipeline = Column(String(100), primary_key=True)
    result = Column(String, nullable=True)
    createdon = Column(DateTime, nullable=False)

def DBPath(servicename):
    dbpath = 'sqlite:///data/' + servicename + '/dumps.db'
    return dbpath

def InitDB(servicename):
    dbpath = DBPath(servicename)
    if os.path.exists(dbpath):
        return

    engine = create_engine('sqlite:///data/logs.db')
    Base.metadata.create_all(engine)