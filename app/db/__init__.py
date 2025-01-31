from os import getenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# The engine variable manages the overall connection to the database
# The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations
# The Base class variable helps us map the models to real MySQL tables

load_dotenv()

# connect to db using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()