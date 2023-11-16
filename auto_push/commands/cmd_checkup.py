import json
import os
import typer
from pathlib import Path
from rich import print
from rich.table import Table

from auto_push.src.classes.storage_manager import StorageManager


# -- Variables
app = typer.Typer(rich_help_panel="rich")
storage_manager = StorageManager()


@app.command(rich_help_panel="Utils & Configs")
def checkup():
    """
    Prints the current environment variable values set in the .env file.
    """
    try:
        # -- Variables
        env_path = Path(__file__).parent.parent.parent / '.env'
        location = storage_manager.get_data("location")
        full_file_path = os.path.join(location, "auto_push.json")

        if env_path.exists():
            print(
                f"[bold underline blue]Current .env file contents:\n[/bold underline blue]")
            table = Table("Key", "Value")
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split("=", 1)
                        table.add_row(
                            f"[yellow]{key}[/yellow]", f"[purple]{value}[/purple]")
            print(table)
        else:
            print("[bold yellow italic]No .env file found.[/bold yellow italic]")

        with open(full_file_path, "r+") as file:
            data = json.load(file)
            table = Table("Key", "Value")
            for key, value in data.items():
                table.add_row(
                    f"[yellow]{key}[/yellow]",
                    "[purple]Activated[/purple]" if value is True else "[purple]Deactivated[/purple]" if value is False else f"[purple]{value}[/purple]"
                )
            print(
                f"[bold underline blue]Current configuration file contents:\n[/bold underline blue]")
            print(table)

    except Exception as e:
        print(
            f"[bold red]An error occurred while reading configuration: {e}[/bold red]")
