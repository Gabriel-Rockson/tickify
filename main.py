#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import name, system
import subprocess
import time

from playsound import playsound
from rich.console import Console
from rich.progress import track
from rich.table import Table
import typer

# Instantiate console
console = Console()

sound_files: dict[str, str] = {
    "work": "./sounds/work-sound.mp3",
    "short-break": "./sounds/short-break-sound.mp3",
    "long-break": "./sounds/long-break-sound.mp3",
}

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


def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
    system("clc" if name == "nt" else "clear")


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


class Pomodoro:
    """
    A class for a pomodoro instance.
    """

    def __init__(
        self,
        pomodoros: int,
        session_rounds: int,
        session_minutes: int,
        short_break_minutes: int,
        long_break_minutes: int,
    ) -> None:
        self.pomodoro_sessions = pomodoros
        self.session_rounds = session_rounds
        self.session_minutes = session_minutes
        self.short_break_minutes = short_break_minutes
        self.long_break_minutes = long_break_minutes
        self.completed_rounds = 0
        self.completed_sessions = 0

    def show_alert(
        self, message: str, urgency: str = "normal"
    ) -> None:  # TODO: Modify to work on both windows and unix
        """
        urgency: low, normal or critical
        """
        subprocess.Popen(["notify-send", "-t", "3000", "-u", f"{urgency}", message])

    def start_session(self) -> None:
        for _ in track(
            range(self.session_minutes * 60),
            description=f"[bold]Round {self.completed_rounds + 1} Tick Tock ...",
        ):
            time.sleep(1)

        self.completed_rounds += 1
        self.show_alert("Round Done, Break Time Coming Up.", urgency="low")
        console.print(f"[bold green]Round {self.completed_rounds} Completed.\n")

    def start_short_break(self) -> None:
        for _ in track(
            range(self.short_break_minutes * 60),
            description=f"[bold]Short Break, Take Some Rest",
        ):
            time.sleep(1)

        self.show_alert("Short Break Over!! Get Back to Work.", urgency="critical")
        console.print(f"[bold green]Short Break Over\n")

    def start_long_break(self) -> None:
        for _ in track(
            range(self.long_break_minutes * 60),
            description=f"[bold]Long Break, Enjoy",
        ):
            time.sleep(1)

        self.show_alert("Long Break Completed.")
        console.print(f"[bold green]Long Break Over.\n")

    def display_rounds_complete_message(self) -> None:
        console.print("[bold blue]ALL ROUNDS HAVE BEEN COMPLETED FOR THIS SESSION\n")

    def display_session_complete_message(self) -> None:
        console.print("[bold green]ALL SESSIONS HAVE BEEN COMPLETED\n")

    def reset_completed_rounds(self) -> None:
        self.completed_rounds = 0

    def play_sound(self, sound_file: str) -> None:
        playsound(sound_file)

    def start(self) -> None:
        for pomodoro_session_count in range(self.pomodoro_sessions):
            clear_screen()
            console.rule(f"[bold]Pomodoro Session {pomodoro_session_count + 1}")

            while self.completed_rounds < self.session_rounds:
                if self.completed_rounds == 0:
                    self.show_alert(
                        "Work about to start, Stay Focused...", urgency="critical"
                    )
                    self.play_sound(sound_files["work"])

                if pomodoro_session_count > 0:
                    self.play_sound(sound_files["work"])

                self.start_session()

                if self.completed_rounds <= self.session_rounds - 1:
                    self.play_sound(sound_files["short-break"])
                    self.start_short_break()

                    self.play_sound(sound_files["work"])

            self.reset_completed_rounds()
            self.display_rounds_complete_message()

            self.play_sound(sound_files["long-break"])
            self.start_long_break()

        console.rule("[bold green]ALL POMODORO SESSIONS COMPLETED")
        self.show_alert("All pomodoro sessions completed successfully.")

        console.print("[bold red]Press any to quit ...")
        input()
        typer.Exit()

    def __str__(self) -> str:
        return f"Pomodoro Timer {self.session_minutes}"


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
