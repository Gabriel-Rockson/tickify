import subprocess
import time

import click

from playsound import playsound
from rich.console import Console
from rich.progress import Progress
import typer

from pomodoro import crud

console = Console()

sound_files: dict[str, str] = {
    "work": "./sounds/work-sound.mp3",
    "short-break": "./sounds/short-break-sound.mp3",
    "long-break": "./sounds/long-break-sound.mp3",
}


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
        self.elasped_round_seconds = 0
        self.elasped_short_break_seconds = 0
        self.elasped_long_break_seconds = 0
        self.run_pomodoro = True

    def show_alert(
        self, message: str, urgency: str = "normal"
    ) -> None:  # TODO: Modify to work on both windows and unix
        """
        urgency: low, normal or critical
        """
        subprocess.Popen(["notify-send", "-t", "3000", "-u", f"{urgency}", message])

    def get_seconds(self, time_in_minutes: int) -> int:
        return time_in_minutes * 60

    def on_press(self, key):
        """
        Method to listen for key presses while the application is running
        """
        try:
            if key.char == "p":
                self.run_pomodoro = not self.run_pomodoro
        except AttributeError:
            pass

    def on_release(self, key):
        pass

    def start_session(self) -> None:
        with Progress() as progress:
            task1 = progress.add_task(
                f"[bold yellow]Round {self.completed_rounds + 1} ...",
                total=self.get_seconds(self.session_minutes),
            )

            while not progress.finished:
                if self.run_pomodoro:
                    progress.update(task1, advance=1)
                    time.sleep(1)

        self.completed_rounds += 1

        self.show_alert("Round Done, Break Time Coming Up.", urgency="low")
        console.print(f"[bold green]Round {self.completed_rounds} Completed.\n")

    def start_short_break(self) -> None:
        with Progress() as progress:
            task1 = progress.add_task(
                f"Short Break ...", total=self.get_seconds(self.short_break_minutes)
            )

            while not progress.finished:
                progress.update(task1, advance=1)
                time.sleep(1)

        self.show_alert("Short Break Over!! Get Back to Work.", urgency="critical")
        console.print(f"[bold green]Short Break Over\n")

    def start_long_break(self) -> None:
        with Progress() as progress:
            task1 = progress.add_task(
                f"Long Break ...", total=self.get_seconds(self.long_break_minutes)
            )

            while not progress.finished:
                progress.update(task1, advance=1)
                time.sleep(1)

        self.show_alert("Long Break Completed.")
        console.print(f"[bold green]Long Break Over.\n")

    def display_rounds_complete_message(self) -> None:
        console.print("[bold blue]ALL ROUNDS HAVE BEEN COMPLETED FOR THIS SESSION\n")

    def display_session_complete_message(self) -> None:
        console.print("[bold green]ALL SESSIONS HAVE BEEN COMPLETED\n")

    def display_round_help_keys(self) -> None:
        console.print(
            "[bold]Help Keys[/bold] \n[bold red]p:[/bold red] "
            "[bold]pause / resume round[/bold]\n[bold red]s:[/bold red] [bold]stop round[/bold]\n"
            "[bold red]b:[/bold red] [bold]skip break[/bold]\n"
        )

    def reset_completed_rounds(self) -> None:
        self.completed_rounds = 0

    def play_sound(self, sound_file: str) -> None:
        playsound(sound_file)

    def get_completed_rounds(self) -> int:
        return self.completed_rounds

    def get_completed_sessions(self) -> int:
        return self.completed_sessions

    def start(self) -> None:
        # Add the data to the database
        record = crud.add_new_record(
            number_of_sessions=self.pomodoro_sessions,
            minutes_per_session=self.session_minutes,
            minutes_per_short_break=self.short_break_minutes,
            minutes_per_long_break=self.long_break_minutes,
            rounds_per_session=self.session_rounds,
        )

        for pomodoro_session_count in range(self.pomodoro_sessions):
            # listener = keyboard.Listener(on_press=self.on_press)
            # listener.start()

            click.clear()
            console.rule(f"[bold]Pomodoro Session {pomodoro_session_count + 1}")
            self.display_round_help_keys()

            while self.completed_rounds < self.session_rounds:
                if self.completed_rounds == 0:
                    self.show_alert(
                        "Work about to start, Stay Focused...", urgency="critical"
                    )
                    self.play_sound(sound_files["work"])

                if pomodoro_session_count > 0:
                    self.play_sound(sound_files["work"])

                self.start_session()

                # Update the databe, and change the completed rounds
                crud.update_record_rounds(id=record.id)  # type: ignore

                # Sound the short break bell only n - 1 times
                if self.completed_rounds <= self.session_rounds - 1:
                    self.play_sound(sound_files["short-break"])
                    self.start_short_break()

                    self.play_sound(sound_files["work"])

            self.completed_sessions += 1

            # After all round, update the total sessions count
            crud.update_record_total_sessions(id=record.id)  # type: ignore

            self.reset_completed_rounds()
            self.display_rounds_complete_message()

            # Sound the long break bell only n - 1 times
            if self.completed_sessions <= self.pomodoro_sessions - 1:
                self.play_sound(sound_files["long-break"])
                self.start_long_break()

        # After all sessions, update done and ended
        crud.update_done_status(id=record.id)  # type: ignore

        console.rule("[bold green]ALL POMODORO SESSIONS COMPLETED")
        self.show_alert("All pomodoro sessions completed successfully.")

        console.print("[bold red]Press any to quit ...")
        input()
        typer.Exit()

    def __str__(self) -> str:
        return f"Pomodoro Timer {self.session_minutes}"
