#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep


import click
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table
import typer

from db.config import engine
from db.models import Base
from pomodoro import crud
from pomodoro.pomodoro import Pomodoro

Base.metadata.create_all(bind=engine)

# Instantiate console
console = Console()


time_options = [
    {
        "round_time": ("15:00", "15 minutes"),
        "short_break": ("3:00", "3 minutes"),
        "long_break": ("10:00", "10 minutes"),
    },
    {
        "round_time": ("15:00", "15 minutes"),
        "short_break": ("5:00", "5 minutes"),
        "long_break": ("10:00", "10 minutes"),
    },
    {
        "round_time": ("25:00", "25 minutes"),
        "short_break": ("5:00", "5 minutes"),
        "long_break": ("10:00", "10 minutes"),
    },
    {
        "round_time": ("30:00", "30 minutes"),
        "short_break": ("5:00", "5 minutes"),
        "long_break": ("10:00", "10 minutes"),
    },
    {
        "round_time": ("30:00", "30 minutes"),
        "short_break": ("10:00", "10 minutes"),
        "long_break": ("15:00", "15 minutes"),
    },
    {
        "round_time": ("45:00", "45 minutes"),
        "short_break": ("10:00", "10 minutes"),
        "long_break": ("15:00", "15 minutes"),
    },
    {
        "round_time": ("45:00", "45 minutes"),
        "short_break": ("10:00", "10 minutes"),
        "long_break": ("20:00", "20 minutes"),
    },
    {
        "round_time": ("60:00", "1 hour"),
        "short_break": ("10:00", "10 minutes"),
        "long_break": ("30:00", "30 minutes"),
    },
]


def display_time_options(options):
    """
    Display the time options for a pomodoro session
    """
    table = Table(
        title="Time Options for Pomodoro Session",
        title_style="bold green",
        show_lines=True,
    )
    table.add_column("Option", style="bold yellow")
    table.add_column("Round Time", style="bold green")
    table.add_column("Short Break Time", style="bold")
    table.add_column("Long Break Time", style="bold")

    for number, option in enumerate(options, start=1):
        table.add_row(
            str(number),
            option["round_time"][1],
            option["short_break"][1],
            option["long_break"][1],
        )

    console.print(table)


def display_program_options():
    table = Table(title="Program Options", title_style="bold green", show_lines=True)

    table.add_column("Option", style="bold blue")
    table.add_column("Title", style="bold")
    table.add_column("Description")

    options: list[dict[str, str]] = [
        {
            "number": "1",
            "option": "Run Pomodoro",
            "description": "Run a new pomodoro session",
        },
        {
            "number": "2",
            "option": "All Statistics",
            "description": "View all previous pomodoro sessions statistics",
        },
        {
            "number": "3",
            "option": "Show Today's Statistics",
            "description": "View the statistics of all pomodoro sessions today",
        },
    ]

    for option in options:
        table.add_row(option["number"], option["option"], option["description"])

    console.print(table)


def start_new_pomodoro_instance():
    click.clear()
    console.rule("[bold]Pomodoro session information")

    session_rounds = int(
        console.input("[bold yellow]How many rounds per session? eg, 4: ")
    )
    print()

    pomodoros = int(
        console.input(
            "[bold yellow]How many pomodoro sessions do you want to run? eg, 2: "
        )
    )
    print()
    # Pomodoro options
    display_time_options(time_options)
    time_option = eval(console.input("[bold yellow]Your time choice, eg, 3: "))

    round_time_option = time_options[time_option - 1]["round_time"][0].split(":")
    short_break_option = time_options[time_option - 1]["short_break"][0].split(":")
    long_break_option = time_options[time_option - 1]["long_break"][0].split(":")

    round_time = int(round_time_option[0])
    short_break = int(short_break_option[0])
    long_break = int(long_break_option[0])

    # Instantiate pomodoro
    pomodoro = Pomodoro(
        pomodoros=pomodoros,
        session_rounds=session_rounds,
        session_minutes=round_time,
        short_break_minutes=short_break,
        long_break_minutes=long_break,
    )

    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task(
            "[bold red]Starting new pomodoro session in ...", total=5
        )

        while not progress.finished:
            sleep(1)
            progress.update(task, advance=1)

    click.clear()

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

    click.clear()
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

    click.clear()
    console.rule(
        f"[bold red]Statistics for: {datetime.today().date().strftime('%A %d %B %Y')}"
    )  # TODO: make the date human readable
    console.print(table)
    print()


def main():
    click.clear()

    # Display program options
    display_program_options()
    option = eval(console.input("[bold yellow]Enter your choice, eg, 1: "))

    if option == 1:
        start_new_pomodoro_instance()
    elif option == 2:
        show_all_statistics()
    elif option == 3:
        show_today_statistics()


if __name__ == "__main__":
    typer.run(main)
