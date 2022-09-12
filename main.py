#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from rich.console import Console
from rich.table import Table
import typer

from db.config import engine
from db.models import Base
from pomodoro import crud
from pomodoro.pomodoro import Pomodoro
from pomodoro.utils import clear_screen

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


def display_program_options():
    table = Table(title="Options", title_style="bold green")

    table.add_column("Option Number", style="bold blue")
    table.add_column("Option", style="magenta bold")
    table.add_column("Description", style="bold italic")

    options: list[dict[str, str]] = [
        {
            "number": "1",
            "option": "Show Today's Statistics",
            "description": "View the statistics of all pomodoro sessions today",
        },
        {
            "number": "2",
            "option": "All Statistics",
            "description": "View all previous pomodoro sessions statistics",
        },
        {
            "number": "3",
            "option": "Run Pomodoro",
            "description": "Run a new pomodoro session",
        },
    ]

    for option in options:
        table.add_row(option["number"], option["option"], option["description"])

    console.print(table)


def start_new_pomodoro_instance():
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


def show_all_statistics():
    all_records = crud.get_all_records()

    table = Table(title="All Records", title_style="bold green")

    table.add_column("Started", style="bold")
    table.add_column("Ended", style="bold")
    table.add_column("Sessions", style="bold blue")
    table.add_column("Rounds Per Session", style="blue")
    table.add_column("Minutes per Round")
    table.add_column("Completed Sessions")
    table.add_column("Completed Rounds")
    table.add_column("Completed")

    for record in all_records:
        table.add_row(
            str(record.started),
            str(record.ended),
            str(record.number_of_sessions),
            str(record.rounds_per_session),
            str(record.minutes_per_session),
            str(record.total_completed_sessions),
            str(record.total_completed_rounds),
            str(record.done),
        )

    clear_screen()
    console.rule("[bold]Statistics")
    console.print(table)


def show_today_statistics():
    records = crud.get_todays_records()

    total_minutes_worked = 0

    table = Table(
        title=f"Pomodoros for Today: {datetime.today().date().strftime('%A %d %B %Y')}",
        title_style="bold green",
        title_justify="left",
    )

    table.add_column("Time Started", style="bold")
    table.add_column("Time Ended", style="bold")
    table.add_column("Sessions", style="bold blue")
    table.add_column("Rounds Per Session", style="bold blue")
    table.add_column("Minutes per Round", style="bold")
    table.add_column("Completed Sessions", style="bold")
    table.add_column("Completed Rounds", style="bold")
    table.add_column("Completed", style="bold")
    table.add_column("Time Spent Working", style="bold green")

    for record in records:
        minutes_worked = record.total_completed_rounds * record.minutes_per_session
        total_minutes_worked += minutes_worked

        table.add_row(
            str(record.started.time()),
            str(record.ended.time() if record.ended else "-"),
            str(record.number_of_sessions),
            str(record.rounds_per_session),
            str(record.minutes_per_session),
            str(record.total_completed_sessions),
            str(record.total_completed_rounds),
            str(record.done),
            f"{minutes_worked} minutes",
        )

    table.caption = f"Total Minutes Worked: {total_minutes_worked}"
    table.caption_style = "yellow"
    table.caption_justify = "right"

    clear_screen()
    console.rule(
        f"[bold red]Statistics for: {datetime.today().date().strftime('%A %d %B %Y')}"
    )  # TODO: make the date human readable
    console.print(table)
    print()


def main():
    clear_screen()

    # Display program options
    display_program_options()
    option = eval(console.input("[bold yellow]Enter your choice, eg, 1: "))

    if option == 1:
        show_today_statistics()
    elif option == 2:
        show_all_statistics()
    elif option == 3:
        start_new_pomodoro_instance()


if __name__ == "__main__":
    typer.run(main)
