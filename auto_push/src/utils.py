import typer
import platform

from auto_push.src.constants import __version__


def print_version(value: bool) -> str:
    if value:
        typer.echo(f"Version: {__version__}")
        raise typer.Exit()

def get_os_system() -> str:
    return platform.system()
