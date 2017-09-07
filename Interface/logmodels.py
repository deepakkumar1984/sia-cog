import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.types import String, DateTime, Integer, Float

Base = declarative_base()

class PredLog(Base):
    __tablename__ = 'predlog'
    id = Column(Integer, primary_key=True, autoincrement=True)
    servicename = Column(String(20), nullable=False)
    servicetype = Column(String(20), nullable=False)
    message = Column(String, nullable=True)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    status = Column(String(20), nullable=False)
    createdon = Column(DateTime, nullable=False)

def DBPath():
    return 'sqlite:///data/logs.db'

def InitDB():
    engine = create_engine(DBPath())
    Base.metadata.create_all(engine)