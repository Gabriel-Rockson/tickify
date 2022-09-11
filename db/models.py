from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.sql import func

from .config import Base


class Pomodoro(Base):
    """
    SQLAlchemy model for the pomodoro table
    """

    __tablename__ = "pomodoros"

    id = Column(Integer, primary_key=True, index=True)
    started = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    ended = Column(DateTime(timezone=True), nullable=True)
    number_of_sessions = Column(Integer, nullable=False)
    minutes_per_session = Column(Integer, nullable=False)
    minutes_per_short_break = Column(Integer, nullable=False)
    minutes_per_long_break = Column(Integer, nullable=False)
    rounds_per_session = Column(Integer, nullable=False)
    completed_rounds = Column(Integer, nullable=False, default=0)
    completed_sessions = Column(Integer, nullable=False, default=0)
    done = Column(Boolean, nullable=False, default=False)

    def __init__(
        self,
        number_of_sessions: int,
        minutes_per_session: int,
        minutes_per_short_break: int,
        minutes_per_long_break: int,
        rounds_per_session: int,
    ):
        self.number_of_sessions = number_of_sessions
        self.minutes_per_session = minutes_per_session
        self.minutes_per_short_break = minutes_per_short_break
        self.minutes_per_long_break = minutes_per_long_break
        self.rounds_per_session = rounds_per_session
