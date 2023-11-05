from plyer import notification
from auto_push.src.classes.github import Github
from auto_push.src.classes.weather import Weather
from auto_push.src.classes.env_loader import EnvLoader

# -- Load .env filec
env_loader = EnvLoader()
env_loader.load_env()

# -- Create weather object
weather = Weather()

# -- Create Github object
github = Github()


def updater():
    print('Updater as been call.')

    # -- Make a request to get the current weather in bangkok.
    response = weather.get_weather()
    github_bio = weather.format_weather(response)

    # -- Make a request to GitHub
    github.update_bio(github_bio)
    github.update_status('Working on Github API.')
    notification.notify(
        'Auto push', 'Your Github bio has been updated successfully.')


if __name__ == '__main__':
    updater()
