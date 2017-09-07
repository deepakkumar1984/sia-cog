import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    createdon = Column(DateTime, nullable=False)
    modifiedon = Column(DateTime, nullable=False)

class PipelineJob(Base):
    __tablename__ = 'pipelinejob'
    id = Column(Integer, primary_key=True)
    servicename = Column(String(20), nullable=False)
    servicetype = Column(String(20), nullable=False)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    message = Column(String, nullable=True)
    status = Column(String(20), nullable=False)
    createdon = Column(DateTime, nullable=False)

class TrainingJob(Base):
    __tablename__ = 'trainingjob'
    id = Column(Integer, primary_key=True)
    servicename = Column(String(20), nullable=False)
    servicetype = Column(String(20), nullable=False)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    totalepoch = Column(Integer, nullable=True)
    result = Column(String, nullable=True)
    learninghistory = Column(String, nullable=True)
    message = Column(String, nullable=True)
    status = Column(String(20), nullable=False)
    createdon = Column(DateTime, nullable=False)

class CurrentTraining(Base):
    __tablename__ = 'currenttraining'
    id = Column(Integer, primary_key=True)
    epoch = Column(Integer, nullable=False)
    loss = Column(Float, nullable=False)

def DBPath():
    return "sqlite:///projects.db"

def InitDB():
    engine = create_engine(DBPath())
    Base.metadata.create_all(engine)
