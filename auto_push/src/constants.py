from pathlib import Path

__version__ = "0.1.0"

# -- Storage
STORAGE_LOCATION_UNIX = f"{Path(__file__).parent.parent.parent}/var"
STORAGE_LOCATION_WINDOWS = ""
STORAGE_LOCATION_LINUX = ""
STORAGE_BASIC_OPTS = {
    "app_init": True,
    "weather_api": False,
    "github_status": False,
    "github_bio_custom_content": False,
    "keyboard_handler": False
}
