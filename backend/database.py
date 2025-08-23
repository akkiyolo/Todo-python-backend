from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - for development, we'll use SQLite for simplicity
# In production, replace with PostgreSQL URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")

# For PostgreSQL, use:
# DATABASE_URL = "postgresql://username:password@localhost/todos"

engine = create_engine(
    DATABASE_URL,
    # SQLite specific - remove for PostgreSQL
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()