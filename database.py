from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SSL_ARGS = {
    "ssl": {
        "ca": "ca.pem"
    }
}

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL,connect_args=SSL_ARGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()