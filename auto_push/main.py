import typer
import sys
from pathlib import Path
from crontab import CronTab
from auto_push.src.updater import updater

# -- Create CLI app
app = typer.Typer()

# -- Create scheduler
scheduler = CronTab(user="ugolin-olle")


@app.command()
def launch():
    job = scheduler.new(f"{sys.executable} {Path.cwd()}/auto_push/src/updater.py")
    job.hour.every(6)
    scheduler.write()


@app.command()
def stop():
    scheduler.remove_all()
    scheduler.write()
    typer.echo('All cron job as been removed successfully.')
