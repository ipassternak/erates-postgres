import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from psycopg2 import pool

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://erates:erates@postgres:5432/erates")

db_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, dsn=DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cursor():
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
    finally:
        db_pool.putconn(conn)