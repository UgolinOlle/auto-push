from plyer import notification
from classes.github import Github
from classes.weather import Weather
from classes.env_loader import EnvLoader


def launch_update():
    print('ok')

    # -- Load .env file
    env_loader = EnvLoader()
    env_loader.load_env()

    # -- Make a request to get weather
    weather = Weather()
    response = weather.get_weather()
    github_bio = weather.format_weather(response)

    # -- Make a request to GitHub
    github = Github()
    github.update_bio(github_bio)
    github.update_status('Working on Github API.')
    notification.notify(
        'Auto push', 'Your Github bio has been updated successfully.')


if __name__ == '__main__':
    launch_update()

