import os

import uvicorn
# from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2

# load_dotenv()
# DB_URL = 'postgresql://postgres:1@localhost/fast_api'
DB_URL = 'sqlite:///todo.sqlite3'

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
