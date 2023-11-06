import typer
from pathlib import Path
from rich import print


# -- Variables
app = typer.Typer(rich_help_panel="rich")


@app.command(rich_help_panel="Utils & Configs")
def setup(key: int = typer.Option(..., help="""
                                  The environment variable key.
                                  1: Gitub personnal access token
                                  2: Weather API key
                                  """),
          value: str = typer.Option(..., help="The environment variable value")):
    """
    Adds a new environment variable to the .env file.

    Parameters:
    key: The key of the environment variable to set.
    value: The value of the environment variable to set.
    """
    try:
        env_path = Path(__file__).parent / '..' / '.env'
        if not env_path.exists():
            env_path.touch()
        with open(env_path, 'a') as f:
            if key == 1:
                f.write(f"GITHUB_PERSONAL_ACCESS={value}\n")
            elif key == 2:
                f.write(f"WEATHER_API_KEY={value}\n")
            elif key != 1 or key != 2:
                print(
                    f"[bold red]An error occurred, {key} is not a good configuration key.[/bold red]")
            else:
                print(
                    f"[bold green]{key} has been set up successfully.[/bold green]")
    except Exception as e:
        print(
            f"[bold red]An error occurred while setting up the environment variable: {e}[/bold red]")
