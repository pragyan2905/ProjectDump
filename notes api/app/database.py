from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# 1. Define the database URL. We use SQLite because it's built-in and requires no setup.
# In a production app, you might use: "postgresql://user:password@localhost/dbname"
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"

# 2. Create the SQLAlchemy "engine". The engine is responsible for actually talking to the DB.
# 'check_same_thread': False is needed only for SQLite in FastAPI since FastAPI can use multiple threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class. Each instance of this class will be a database session.
# We will use this in a dependency to get a new session for every request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class. All our database models (tables) will inherit from this Base.
# SQLAlchemy will use this Base to keep track of all the tables we define.
Base = declarative_base()

# 5. Dependency to get the DB session. This is a generator function.
# It ensures that a database connection is opened for a request and closed when the request is done.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
