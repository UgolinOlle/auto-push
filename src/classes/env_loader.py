import os
from dotenv import load_dotenv


class EnvLoader:
    """
    Class for loading and validating environment variables.
    """

    def load_env(self) -> None:
        """
        Loads environment variables from a .env file and validates them.
        """
        load_dotenv()
        self.validate(os.environ)

    def validate(self, env: os._Environ[str]) -> None:
        """
        Validates the necessary environment variables.

        Parameters:
            env (os._Environ[str]): The environment variables to validate.

        Raises:
            Exception: If required environment variables are missing.
        """
        if not env.get("GITHUB_PERSONAL_ACCESS"):
            raise Exception("Github access token hasn't been provided.")
        if not env.get("WEATHER_API_KEY"):
            raise Exception("Weather API key hasn't been provided.")
