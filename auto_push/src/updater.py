from plyer import notification
from auto_push.src.classes.github import Github
from auto_push.src.classes.weather import Weather

# -- Create weather object
weather = Weather()

# -- Create Github object
github = Github()


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
    print('Updater has been called.')

    # -- Make a request to get the current weather in Bangkok.
    response = weather.get_weather()
    github_bio = weather.format_weather(response)

    # -- Update GitHub bio with the weather information
    github.update_bio(github_bio)

    # -- Update GitHub status
    github.update_status('Working on Github API.')

    # -- Send a notification to the user
    notification.notify(
        title='Auto push',
        message='Your Github bio has been updated successfully.'
    )


if __name__ == '__main__':
    updater()
