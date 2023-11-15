import os
import typer
from crontab import CronTab
from rich import print

from auto_push.src.classes.storage_manager import StorageManager


# -- Variables
app = typer.Typer(rich_help_panel="rich")
storage_manager = StorageManager()
current_user = os.getlogin()
scheduler = CronTab(user=current_user)


@app.command(rich_help_panel="Commands")
def stop():
    """
    Stops and removes all cron jobs for the current user.
    """
    scheduler.remove_all()
    scheduler.write()
    storage_manager.set_data("github_cron_tab", False)
    print('[bold green]All cron jobs have been removed successfully.[/bold green]')
