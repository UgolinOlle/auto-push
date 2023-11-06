import os
import sys
import typer
from crontab import CronTab
from pathlib import Path
from rich import print


# -- Variables
app = typer.Typer(rich_help_panel="rich")
current_user = os.getlogin()
scheduler = CronTab(user=current_user)


@app.command(rich_help_panel="Commands")
def start():
    """
    [green]Create[/green] cron job to run the updater script every 6 hours.
    """
    try:
        script_path = Path.cwd() / "auto_push" / "src" / "updater.py"
        job = scheduler.new(command=f"{sys.executable} {script_path}")
        job.hour.every(6)
        scheduler.write()
        print('[bold green]Github bio update has been set successfully.[/bold green]')
    except Exception as e:
        print(
            f"[bold red]An error occurred while setting up the cron job: {e}[/bold red]")
