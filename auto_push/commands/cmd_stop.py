import os
import typer
from crontab import CronTab
from rich import print


# -- Variables
app = typer.Typer(rich_help_panel="rich")
current_user = os.getlogin()
scheduler = CronTab(user=current_user)


@app.command(rich_help_panel="Commands")
def stop():
    """
    Stops and removes all cron jobs for the current user.
    """
    scheduler.remove_all()
    scheduler.write()
    print('[bold green]All cron jobs have been removed successfully.[/bold green]')
