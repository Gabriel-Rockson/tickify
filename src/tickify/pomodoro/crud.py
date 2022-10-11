from datetime import date

from sqlalchemy.sql import func

from tickify.db.config import SessionLocal
from tickify.db.models import Pomodoro


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


def update_record_rounds(id: int):
    """
    Given the id of a record, increase its rounds count.
    """

    with SessionLocal() as session:
        query = session.query(Pomodoro).filter(Pomodoro.id == id)
        pomodoro = query.first()

        query.update({"total_completed_rounds": pomodoro.total_completed_rounds + 1})  # type: ignore
        session.commit()


def update_record_total_sessions(id: int):
    """
    Given the id of a record, increase its total sessions count.
    """

    with SessionLocal() as session:
        query = session.query(Pomodoro).filter(Pomodoro.id == id)
        pomodoro = query.first()

        query.update({"total_completed_sessions": pomodoro.total_completed_sessions + 1})  # type: ignore
        session.commit()


def update_done_status(id: int):
    """
    Given the id of a record, mark the pomodoro as done.
    """

    with SessionLocal() as session:
        query = session.query(Pomodoro).filter(Pomodoro.id == id)

        query.update({"done": True, "ended": func.now()})
        session.commit()


def get_all_records():
    """
    Fetch all statistics from the database.
    """

    with SessionLocal() as session:
        all_records = session.query(Pomodoro).all()

    return all_records


def get_todays_records():
    """
    Fetch all records today from the database.
    """

    with SessionLocal() as session:
        records = (
            session.query(Pomodoro)
            .filter(func.date(Pomodoro.started) == date.today())
            .all()
        )

    return records
