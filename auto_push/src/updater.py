import os
from plyer import notification
from rich import print

from auto_push.src.classes.env_loader import EnvLoader
from auto_push.src.classes.github import Github
from auto_push.src.classes.storage_manager import StorageManager
from auto_push.src.classes.weather import Weather

# -- Load .env file
env_loader = EnvLoader()
env_loader.load_env()

# -- Create all object
weather = Weather()
github = Github()
storage_manager = StorageManager()


def updater():
    """
    Updates the GitHub bio with the current weather information and sends a notification.

    The function fetches the current weather, formats it, and then updates the GitHub bio
    with this formatted weather information. After updating GitHub, it also sets the GitHub
    status to a specific message and sends a desktop notification to inform the user of
    successful completion.

    The weather information is fetched for Bangkok, and the GitHub objects are initialized
    with environmental variables loaded at the beginning of the script.
    """

    try:
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
            print("[bold red]There is an error in the configuration file. You cannot have custom content and weather api set in same time.[/bold red]")

        # -- Update GitHub bio with the weather information
        github.update_bio(github_bio)

        # -- Update GitHub status
        github.update_status('Working on Github API.')

        # -- Send a notification to the user
        notification.notify(
            title='Auto push',
            message='Your Github bio has been updated successfully.'
        )
    except Exception as e:
        print(
            f"[bold red]An error occurred during update Github bio. Support as been already informed.[/bold red]")


if __name__ == '__main__':
    updater()
