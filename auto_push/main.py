import typer

from auto_push.src.classes.storage_manager import StorageManager
from auto_push.src.utils import print_version
from auto_push.commands import cmd_checkup, cmd_setup, cmd_start, cmd_stop


# -- Variables
app = typer.Typer(rich_help_panel="rich")
storage_manager = StorageManager()

# -- Init storage
storage_manager.init_storage()

# -- Add all commands
app.command()(cmd_checkup.checkup)
app.command()(cmd_setup.setup)
app.command()(cmd_start.start)
app.command()(cmd_stop.stop)


@app.callback()
def main(version: bool = typer.Option(None, "--version", callback=print_version, is_eager=True)):
    """
    Run the application.
    """
    pass
