from os import name, system

from rich.console import Console

console = Console()


def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
    system("clc" if name == "nt" else "clear")
