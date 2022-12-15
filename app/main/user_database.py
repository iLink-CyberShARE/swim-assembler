"""Initialize user database connections"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import config_by_name

environment = (os.getenv('BOILERPLATE_ENV') or 'dev')
settings = config_by_name[environment]

engine = create_engine(settings.USER_DATABASE_URL)

user_db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = user_db_session.query_property()