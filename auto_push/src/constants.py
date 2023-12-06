from pathlib import Path

"""
Configuration for storage and basic options for the application.

This module sets up various configurations related to storage and default options for the application. It defines paths for storage based on different operating systems and sets default values for various application settings.

Attributes:
----------
__version__ (str): Indicates the current version of the application.

STORAGE_LOCATION_UNIX (str): The file path for storage on Unix-based systems.
    It is dynamically set relative to the location of this script file.

STORAGE_LOCATION_WINDOWS (str): The file path for storage on Windows systems.
    Currently, this is set as an empty string, indicating no default path is set.

STORAGE_LOCATION_LINUX (str): The file path for storage on Linux systems.
    Currently, this is set as an empty string, indicating no default path is set.

STORAGE_BASIC_OPTS (dict): A dictionary containing basic configuration options for the application.
    These options include flags for app initialization, weather API usage, GitHub status updates,
    custom content for GitHub bio, and keyboard handler activation.

Notes:
-----
- The storage locations for Windows and Linux are placeholders and should be configured as needed.
- The '__version__' attribute should be updated with each new release of the application.
- The 'STORAGE_BASIC_OPTS' dictionary serves as a central place to manage the application's default settings.
"""

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
