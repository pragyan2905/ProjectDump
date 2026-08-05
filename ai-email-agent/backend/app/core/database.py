import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# In production, this comes from your .env file (e.g., postgresql://user:password@localhost/dbname)
# For immediate local development without installing PostgreSQL, we use SQLite as a drop-in replacement.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./email_agent.db")

# 1. Engine: The core interface to the database. It handles the connection pool.
# connect_args={"check_same_thread": False} is a specific requirement for SQLite in FastAPI.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 2. SessionLocal: A factory that creates independent database sessions for each API request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base: The parent class that all our Python DB models will inherit from.
Base = declarative_base()

# 4. Dependency Injection: FastAPI will use this to open/close DB sessions per request safely.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
