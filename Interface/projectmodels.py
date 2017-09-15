from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.types import String, DateTime, Integer, Float

Base = declarative_base()

class Service(Base):
    __tablename__ = 'service'
    servicename = Column(String(20), primary_key=True)
    servicetype = Column(String(20), primary_key=True)
    servicedata = Column(String, nullable=False)
    createdon = Column(DateTime, nullable=False)
    modifiedon = Column(DateTime, nullable=False)

class Pipeline(Base):
    __tablename__ = 'pipeline'
    servicename = Column(String(20), primary_key=True)
    servicetype = Column(String(20), primary_key=True)
    pipelinedata = Column(String, nullable=False)
    pipelineflow = Column(String, nullable=True)
    createdon = Column(DateTime, nullable=False)
    modifiedon = Column(DateTime, nullable=False)

class DeepModel(Base):
    __tablename__ = 'deepmodel'
    servicename = Column(String(20), primary_key=True)
    servicetype = Column(String(20), primary_key=True)
    modelname = Column(String(20), primary_key=True)
    modeldata = Column(String, nullable=False)
    modelflow = Column(String, nullable=False)
    createdon = Column(DateTime, nullable=False)
    modifiedon = Column(DateTime, nullable=False)

class TrainingJob(Base):
    __tablename__ = 'trainingjob'
    id = Column(String, primary_key=True)
    servicename = Column(String(20), nullable=False)
    servicetype = Column(String(20), nullable=False)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    totalepoch = Column(Integer, nullable=True)
    result = Column(String, nullable=True)
    modelhistory = Column(String, nullable=True)
    message = Column(String, nullable=True)
    status = Column(String(20), nullable=False)
    createdon = Column(DateTime, nullable=False)

class CurrentTraining(Base):
    __tablename__ = 'currenttraining'
    id = Column(Integer, primary_key=True)
    epoch = Column(Integer, nullable=False)
    loss = Column(Float, nullable=False)

class LoginUser(Base):
    __tablename__ = 'loginuser'
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    createdon = Column(DateTime, nullable=False)
    modifiedon = Column(DateTime, nullable=False)

class Setting(Base):
    __tablename__ = 'setting'
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)

def DBPath():
    return "sqlite:///./data/projects.db"

def InitDB():
    engine = create_engine(DBPath())
    Base.metadata.create_all(engine)
