from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost/pizaa-delivery')

Base = declarative_base()

Session = sessionmaker()
