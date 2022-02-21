from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import time

import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings as st

SQLALCHEMY_DATABASE_URL = f"postgresql://{st.database_username}:{st.database_password}@{st.database_hostname}:{st.database_port}/{st.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="admin123", cursor_factory=RealDictCursor)
            cur = conn.cursor()
            print("Successfully connected to the database")
            break
        except Exception as e:
            time.sleep(2)
            print(f"Failed to connect: {e}")