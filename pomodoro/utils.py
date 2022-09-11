from os import system, name


def clear_screen() -> None:
    """
    Clear the terminal screen.
    """
    system("clc" if name == "nt" else "clear")
