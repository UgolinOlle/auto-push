import typer
from crontab import CronTab
from pathlib import Path

# -- Create cron object
cron = CronTab(user="ugolin-olle")

# -- Create CLI app
app = typer.Typer()


@app.command()
def launch():
    job = cron.new(command=f'python {Path.cwd()}/src/updater.py')
    job.minute.every(1)
    cron.write()
    typer.echo('Job has been launched successfully.')


@app.command()
def stop_all():
    cron.remove_all()
    cron.write()
    typer.echo('All jobs have been removed.')


@app.command()
def show_all():
    for job in cron:
        type.echo(job)
