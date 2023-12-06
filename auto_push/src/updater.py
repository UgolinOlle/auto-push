from plyer import notification
from rich import print

from auto_push.src.classes.env_loader import EnvLoader
from auto_push.src.classes.github import Github
from auto_push.src.classes.storage_manager import StorageManager
from auto_push.src.classes.weather import Weather
from auto_push.src.decorators.error_issue import error_issue

# -- Load .env file
env_loader = EnvLoader()
env_loader.load_env()

# -- Create all object
weather = Weather()
github = Github()
storage_manager = StorageManager()


@error_issue(github)
def updater():
    """
    Updates the GitHub bio with either custom content or current weather information and sends a desktop notification.

    This function first checks the configuration to determine whether to use custom content or weather information for the GitHub bio. If using weather information, it fetches the current weather data for Bangkok, formats it, and updates the GitHub bio with this information. In case of custom content, it retrieves and sets the pre-defined content from the storage manager. The function also handles any configuration errors by setting the GitHub bio to an empty string and printing an error message.

    After updating the GitHub bio, the function updates the GitHub status message and sends a desktop notification to inform the user that the bio has been updated successfully.

    The function is decorated with `error_issue`, which automatically creates a GitHub issue if an exception occurs during execution.

    Attributes:
    -----------
    github_bio_custom_content (bool): Flag to determine whether to use custom content or weather information.
    weather_api (bool): Flag to indicate if weather API should be used for fetching weather data.
    github_bio (str): The content to be updated in the GitHub bio.

    Raises:
    -------
    Exception: Propagates any exceptions caught during execution to the `error_issue` decorator.
    """
    github_bio_custom_content = storage_manager.get_data(
        "github_bio_custom_content")
    weather_api = storage_manager.get_data("weather_api")

    if github_bio_custom_content is True and weather_api is False:
        github_bio = storage_manager.get_data("github_bio_content")
    elif github_bio_custom_content is False and weather_api is True:
        # -- Make a request to get the current weather in Bangkok.
        response = weather.get_weather()
        github_bio = weather.format_weather(response)
    else:
        github_bio = ""
        print(
            "[bold red]There is an error in the configuration file. You cannot have custom content and weather api set in same time.[/bold red]"
        )

    # -- Update GitHub status
    github.update_bio(content=github_bio)

    # -- Send a notification to the user
    notification.notify(
        title="Auto push", message="Your Github bio has been updated successfully."
    )


if __name__ == "__main__":
    updater()
