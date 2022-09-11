from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    "sqlite:///pomodoro.db", connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """
    Get a session connection to the database
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()  # TODO: this is supposed to close the session


Base = declarative_base()
