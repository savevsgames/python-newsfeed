from os import getenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

# The engine variable manages the overall connection to the database
# The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations
# The Base class variable helps us map the models to real MySQL tables

load_dotenv()

# connect to db using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Creates all the tables mapped in the Base
def init_db(app):
  Base.metadata.create_all(engine)
  # on closed connection - remove db from context with close_db method
  app.teardown_appcontext(close_db)

def get_db():
  # check to see if db exists in global/Flask context
  if 'db' not in g:
    # store new db connection in app context
    g.db = Session()

  return g.db

# kill db connection in context
def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()