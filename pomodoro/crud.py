from db.config import SessionLocal
from db.models import Pomodoro


def add_new_record(
    number_of_sessions: int,
    minutes_per_session: int,
    minutes_per_short_break: int,
    minutes_per_long_break: int,
    rounds_per_session: int,
):
    pomodoro = Pomodoro(
        number_of_sessions=number_of_sessions,
        minutes_per_session=minutes_per_session,
        minutes_per_short_break=minutes_per_short_break,
        minutes_per_long_break=minutes_per_long_break,
        rounds_per_session=rounds_per_session,
    )

    with SessionLocal() as session:
        session.add(pomodoro)
        session.commit()
        session.refresh(pomodoro)

    return pomodoro
