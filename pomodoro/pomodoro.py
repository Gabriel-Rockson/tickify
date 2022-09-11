import subprocess
import time

from playsound import playsound
from rich.console import Console
from rich.progress import track
import typer

from pomodoro import crud
from pomodoro.utils import clear_screen

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
        # Add the data to the database
        record = crud.add_new_record(
            number_of_sessions=self.pomodoro_sessions,
            minutes_per_session=self.session_minutes,
            minutes_per_short_break=self.short_break_minutes,
            minutes_per_long_break=self.long_break_minutes,
            rounds_per_session=self.session_rounds,
        )

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
