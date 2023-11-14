import os
from dotenv import load_dotenv
from rich import print


class EnvLoader:
    """
    Class for loading and validating environment variables.
    """

    def load_env(self) -> None:
        """
        Loads environment variables from a .env file and validates them.
        """
        load_dotenv()
        try:
            self.validate(os.environ)
        except ValueError as e:
            print(f"[bold red]Error: {e}[/bold red]")

    def validate(self, env: os._Environ[str]) -> None:
        """
        Validates the necessary environment variables.

        Parameters:
        -----------
            env (os._Environ[str]): The environment variables to validate.

        Raises:
        -------
            ValueError: If required environment variables are missing.
        """
        required_keys = ["GITHUB_PERSONAL_ACCESS", "WEATHER_API_KEY"]
        for key in required_keys:
            if not env.get(key):
                raise ValueError(
                    f"Required environment variable '{key}' is missing. Please set it in your .env file.")
