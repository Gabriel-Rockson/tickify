#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich.console import Console
from rich.table import Table
import typer

from pomodoro.pomodoro import Pomodoro
from pomodoro.utils import clear_screen

from db.config import engine
from db.models import Base

Base.metadata.create_all(bind=engine)

# Instantiate console
console = Console()


session_time_options: list[dict[str, str]] = [
    {"time": "15:00", "english": "15 minutes"},
    {"time": "20:00", "english": "20 minutes"},
    {"time": "25:00", "english": "25 minutes"},
    {"time": "30:00", "english": "30 minutes"},
    {"time": "35:00", "english": "35 minutes"},
    {"time": "40:00", "english": "40 minutes"},
    {"time": "45:00", "english": "45 minutes"},
    {"time": "50:00", "english": "50 minutes"},
    {"time": "55:00", "english": "55 minutes"},
    {"time": "60:00", "english": "1 hour"},
]

session_short_break_options: list[dict[str, str]] = [
    {"time": "3:00", "english": "3 minutes"},
    {"time": "5:00", "english": "5 minutes"},
    {"time": "10:00", "english": "10 minutes"},
    {"time": "15:00", "english": "15 minutes"},
]

session_long_break_options: list[dict[str, str]] = [
    {"time": "5:00", "english": "5 minutes"},
    {"time": "10:00", "english": "10 minutes"},
    {"time": "15:00", "english": "15 minutes"},
    {"time": "20:00", "english": "20 minutes"},
    {"time": "25:00", "english": "25 minutes"},
]


def display_time_options(options: list[dict[str, str]], title: str) -> None:
    """
    Display the options for the program
    """
    table = Table(title=title, title_style="bold green")

    table.add_column("Option", style="bold blue")
    table.add_column("Time", style="bold")
    table.add_column("English Format", style="bold")

    for number, option in enumerate(options, start=1):
        table.add_row(str(number), option["time"], option["english"])

    console.print(table)


def get_session_time_minutes() -> int:
    session_time_option = int(
        console.input("[bold yellow]Choose your session time, eg, 3: ")
    )

    session_time = session_time_options[session_time_option - 1]
    session_minutes = int(session_time["time"].split(":")[0])

    return session_minutes


def get_short_break_minutes() -> int:
    short_break_option = int(
        console.input("[bold yellow]Choose your short break time, eg, 2: ")
    )
    short_break_time = session_short_break_options[short_break_option - 1]
    short_break_minutes = int(short_break_time["time"].split(":")[0])

    return short_break_minutes


def get_long_break_minutes() -> int:
    long_break_option = int(
        console.input("[bold yellow]Choose your short break time, eg, 2: ")
    )
    long_break_time = session_long_break_options[long_break_option - 1]
    long_break_minutes = int(long_break_time["time"].split(":")[0])

    return long_break_minutes


def main():
    clear_screen()

    # Session time options
    display_time_options(session_time_options, "Session Time Options")
    session_minutes = get_session_time_minutes()

    # Short break session options
    clear_screen()
    display_time_options(session_short_break_options, "Short Break Options")
    short_break_minutes = get_short_break_minutes()

    # Long break session options
    clear_screen()
    display_time_options(session_long_break_options, "Long Break Options")
    long_break_minutes = get_long_break_minutes()

    clear_screen()
    pomodoros = int(console.input("[bold yellow]How many pomodoro sessions? eg, 2 "))
    session_rounds = int(
        console.input("[bold yellow]How many rounds per session? eg, 4 ")
    )

    pomodoro = Pomodoro(
        pomodoros=pomodoros,
        session_rounds=session_rounds,
        session_minutes=session_minutes,
        short_break_minutes=short_break_minutes,
        long_break_minutes=long_break_minutes,
    )

    clear_screen()
    pomodoro.start()


if __name__ == "__main__":
    typer.run(main)
