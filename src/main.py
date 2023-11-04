import typer
from crontab import CronTab

# -- Create cron object
cron = CronTab(user="ugolin-olle")

# -- Create CLI app
app = typer.Typer()


@app.command()
def launch():
    job = cron.new(command='python ./src/updater.py')
    job.minute.every(1)
    cron.write()
    print('Job has been launched successfully.')


@app.command()
def stop_all():
    cron.remove_all()
    cron.write()
    print('All jobs have been removed.')


if __name__ == '__main__':
    app()
