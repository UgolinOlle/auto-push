import typer

from auto_push.src.constants import __version__


def print_version(value: bool):
    if value:
        typer.echo(f"Version: {__version__}")
        raise typer.Exit()
