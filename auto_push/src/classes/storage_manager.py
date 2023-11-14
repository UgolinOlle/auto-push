import json
import os
from typing import Any

from auto_push.src.constants import STORAGE_LOCATION_UNIX, STORAGE_LOCATION_WINDOWS, STORAGE_LOCATION_LINUX
from auto_push.src.utils import get_os_system


class StorageManager:
    """
    A class used to manage storage for the auto_push application.

    This class is responsible for initializing storage based on the operating system,
    and provides methods to set and get data in a JSON file.

    Attributes:
    -----------
    system : str
        The name of the operating system.
    location : str
        The file path where the storage will be initialized.
    storage_file : str
        The name of the JSON file used for storage.
    """

    def __init__(self) -> None:
        """Initializes the StorageManager with system, location, and storage_file attributes."""
        self.system: str = get_os_system()
        self.location: str = ""
        self.storage_file: str = "auto_push.json"

    def init_storage(self) -> None:
        """
        Initializes the storage by creating a directory and a JSON file based on the operating system.

        Creates the necessary directory structure and initializes a JSON file with
        default data if it doesn't exist. If the file exists, it ensures that the 'app_init'
        key is set to True.
        """
        if self.system == "Darwin":
            self.location = STORAGE_LOCATION_UNIX
        elif self.system == "Windows":
            self.location = STORAGE_LOCATION_WINDOWS
        elif self.system == "Linux":
            self.location = STORAGE_LOCATION_LINUX

        os.makedirs(self.location, exist_ok=True)

        full_file_path = os.path.join(self.location, self.storage_file)

        if not os.path.exists(full_file_path):
            with open(full_file_path, 'w') as file:
                json.dump({"app_init": True}, file)
        else:
            with open(full_file_path, 'r+') as file:
                data = json.load(file)
                data["app_init"] = True
                file.seek(0)
                json.dump(data, file)
                file.truncate()

    def set_data(self, key: str, value: Any) -> None:
        """
        Sets the value of a specified key in the JSON storage file.

        Parameters:
        -----------
        key : str
            The key for which the value needs to be set.
        value : Any
            The value to be set for the given key.

        This method will update the JSON file with the new key-value pair.
        If the key already exists, its value will be updated.
        """
        full_file_path = os.path.join(self.location, self.storage_file)

        with open(full_file_path, 'r+') as file:
            data = json.load(file)
            data[key] = value
            file.seek(0)
            json.dump(data, file)
            file.truncate()

    def get_data(self, key: str) -> Any:
        """
        Retrieves the value for a specified key from the JSON storage file.

        Parameters:
        -----------
        key : str
            The key for which the value is to be retrieved.

        Returns:
        --------
        Any
            The value associated with the specified key. Returns None if the key does not exist.
        """
        full_file_path = os.path.join(self.location, self.storage_file)

        with open(full_file_path, 'r') as file:
            data = json.load(file)
            return data.get(key, None)
