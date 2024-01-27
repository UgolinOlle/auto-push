import os
import sys
from pathlib import Path

import typer
from crontab import CronTab
from rich import print

from auto_push.src.classes.storage_manager import StorageManager

# -- Variables
app = typer.Typer(rich_help_panel="rich")
storage_manager = StorageManager()
# current_user = os.getlogin()
scheduler = CronTab(user=True)


def github_update(minute: int = 0, hour: int = 0, day: int = 0, month: int = 0):
    """
    Set up a cron job with the specified scheduling.
    """
    script_path = Path.cwd() / "auto_push" / "src" / "updater.py"

    # -- Setting up the cron job
    job = scheduler.new(command=f"{sys.executable} {script_path}", comment="1")
    job.minute.on(minute if 0 <= minute <= 59 else 0)
    job.hour.on(hour if hour > 0 else 1)
    job.day.on(day if 0 > day <= 31 else 1)
    job.month.on(month if 0 > month <= 31 else 1)
    scheduler.write()

    # -- Execute one time the script
    os.system(f"{sys.executable} {script_path}")


@app.command()
def start(
    content: str = typer.Option("", help="Content to set in your Github bio"),
    minute: int = typer.Option(0, help="Minute for scheduling"),
    hour: int = typer.Option(6, help="Hour for scheduling"),
    day: int = typer.Option(0, help="Day for scheduling"),
    month: int = typer.Option(0, help="Month for scheduling"),
):
    """
    Create or reset a cron job to run the updater script.

    Parameters:
        content: The content of your Github bio.
        minute: The minute when the cron job should run. Defaults to 0.
        hour: The hour when the cron job should run. Defaults to 6.
        day: The day of the month when the cron job should run. Defaults to 0 (every day).
        month: The month when the cron job should run. Defaults to 0 (every month).
    """
    try:
        user_job: str = storage_manager.get_data("github_cron_tab")

        if content != "":
            storage_manager.set_data("github_bio_custom_content", True)
            storage_manager.set_data("github_bio_content", content)
            storage_manager.set_data("weather_api", False)
        else:
            storage_manager.set_data("github_bio_custom_content", False)
            storage_manager.set_data("weather_api", True)
        if user_job is not True:
            github_update(minute=minute, hour=hour, day=day, month=month)
            storage_manager.set_data("github_cron_tab", True)
            print(
                "[bold green]Github bio update has been set successfully.[/bold green]"
            )
        elif user_job is None:
            print(
                "[bold red]An error occured in your configuration file. Automatically reset cli config...[/bold red]"
            )
            storage_manager.fix_storage()
            print(
                "[bold green]CLI configuration as been reset successfully.[/bold green]"
            )
        else:
            print("[bold yellow]Github bio update is already setup.[/bold yellow]")
            reset = typer.prompt("Do you want to reset ? (yes/no)")
            if reset.lower() == "yes":
                scheduler.remove_all(comment="1")
                github_update(minute=minute, hour=hour, day=day, month=month)
                print(
                    "[bold green]Github bio update has been reset successfully.[/bold green]"
                )
    except Exception as e:
        print(
            f"[bold red]An error occurred while setting up the cron job. Sorry for this, we already send a message to support.[/bold red]"
        )
