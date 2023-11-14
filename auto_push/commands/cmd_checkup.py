import os
import typer
from pathlib import Path
from rich import print
from rich.table import Table


# -- Variables
app = typer.Typer(rich_help_panel="rich")


@app.command(rich_help_panel="Utils & Configs")
def checkup():
    """
    Prints the current environment variable values set in the .env file.
    """
    try:
        env_path = Path(__file__).parent.parent.parent / '.env'
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
    except Exception as e:
        print(
            f"[bold red]An error occurred while reading the .env file: {e}[/bold red]")
