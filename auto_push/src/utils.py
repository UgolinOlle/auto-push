import typer
import platform

from auto_push.src.constants import __version__


def print_version(value: bool) -> None:
    """
    Prints the current version of the application and exits if the specified value is True.

    This function is typically used as a command line interface (CLI) option to allow users to check the version of the application. If the 'value' argument is True, it prints the version number and then gracefully exits the application using Typer's built-in exit functionality.

    Parameters:
    ----------
    value (bool): A flag indicating whether to print the version information and exit. If True, the version is printed and the application exits.

    Returns:
    --------
    None
    """
    if value:
        typer.echo(f"Version: {__version__}")
        raise typer.Exit()


def get_os_system() -> str:
    """
    Returns the name of the operating system platform being used.

    This function uses the 'platform' module to determine and return the name of the operating system that the application is running on. This can be useful for making decisions based on the operating system, such as setting file paths or executing OS-specific commands.

    Returns:
    --------
    str: A string representing the name of the operating system.
    """
    return platform.system()
