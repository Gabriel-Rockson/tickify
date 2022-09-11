from sqlalchemy import Column, DateTime, Integer, TIMESTAMP
from sqlalchemy.sql.expression import text

from .config import Base


class Pomodoro(Base):
    """
    SQLAlchemy model for the pomodoro table
    """

    __tablename__ = "pomodoro"

    id = Column(Integer, primary_key=True, index=True)
    started = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    completed = Column(DateTime, nullable=True)
    number_of_sessions = Column(Integer, nullable=False)
    minutes_per_session = Column(Integer, nullable=False)
    minutes_per_short_break = Column(Integer, nullable=False)
    minutes_per_long_break = Column(Integer, nullable=False)
    rounds_per_session = Column(Integer, nullable=False)
    completed_rounds = Column(Integer, nullable=False, default=0)
    completed_sessions = Column(Integer, nullable=False, default=0)
