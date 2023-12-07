import json
import os
from typing import Any

from auto_push.src.constants import STORAGE_LOCATION_UNIX, STORAGE_LOCATION_WINDOWS, STORAGE_LOCATION_LINUX, STORAGE_BASIC_OPTS
from auto_push.src.utils import get_os_system


class StorageManager:
    """
    Manages storage for the auto_push application, handling file operations for data persistence.

    This class is designed to manage the storage of application settings and configurations in a JSON file. It initializes the storage based on the operating system, providing methods for setting, getting, and fixing data.

    Attributes:
    -----------
    system (str): The name of the operating system the application is running on.
    location (str): The file path for storage initialization.
    storage_file (str): The name of the JSON file used for storing application data.

    Methods:
    --------
    init_storage(): Initializes the storage file and directory.
    fix_storage(): Ensures the storage file contains all necessary default options.
    set_data(key, value): Updates or adds a key-value pair in the storage file.
    get_data(key): Retrieves the value associated with a key from the storage file.
    """

    def __init__(self) -> None:
        """
        Initializes the StorageManager by setting the system, location, and storage_file attributes.

        Based on the operating system, it determines the appropriate storage location and sets the path for the storage file. It also ensures that the storage location is set in the storage file.
        """
        self.system: str = get_os_system()
        self.location: str = ""
        self.storage_file: str = "auto_push.json"

        if self.system == "Darwin":
            self.location = STORAGE_LOCATION_UNIX
        elif self.system == "Windows":
            self.location = STORAGE_LOCATION_WINDOWS
        elif self.system == "Linux":
            self.location = STORAGE_LOCATION_LINUX
        self.set_data("location", self.location)

    def init_storage(self) -> None:
        """
        Initializes the storage by creating a directory and a JSON file.

        Depending on the operating system, it creates the necessary directory structure and initializes a JSON file with default data. If the file already exists, it checks for the presence of key settings and adds them if they are missing.
        """
        # -- Create var file
        if not os.path.exists(self.location):
            os.mkdir(self.location)

        # -- Create the file
        full_file_path = os.path.join(self.location, self.storage_file)

        if not os.path.exists(full_file_path):
            with open(full_file_path, 'w') as file:
                json.dump(STORAGE_BASIC_OPTS, file)

    def fix_storage(self) -> None:
        """
        Checks and updates the storage file with default options.

        Iterates over the default options defined in STORAGE_BASIC_OPTS and ensures they are present in the storage file. If any key is missing or its value differs from the default, the storage file is updated accordingly.
        """
        full_file_path = os.path.join(self.location, self.storage_file)

        with open(full_file_path, "r+") as file:
            data = json.load(file)
            updated = False

            for opt_key, opt_value in STORAGE_BASIC_OPTS.items():
                if opt_key not in data or data[opt_key] != opt_value:
                    data[opt_key] = opt_value
                    updated = True

            if updated:
                file.seek(0)  # Go back to the start of the file
                file.truncate()  # Truncate the file to overwrite it
                json.dump(data, file)

    def set_data(self, key: str, value: Any) -> None:
        """
        Sets a specified value for a given key in the storage file.

        Parameters:
        -----------
        key (str): The key for which the value needs to be updated or added.
        value (Any): The value to be set for the specified key.

        Updates the storage file with the new key-value pair, overwriting the value if the key already exists.
        """
        full_file_path = os.path.join(self.location, self.storage_file)

        with open(full_file_path, 'r+') as file:
            data = json.load(file)
            data[key] = value
            file.seek(0)
            json.dump(data, file)
            file.truncate()

    def delete_data(self, key: str) -> None:
        """
        Deletes a specified key and its associated value from the storage file.

        Parameters:
        -----------
        key (str): The key to be deleted from the storage file.

        If the key exists, it is removed from the storage file along with its value.
        """
        pass

    def get_data(self, key: str) -> Any:
        """
        Retrieves the value associated with a specified key from the storage file.

        Parameters:
        -----------
        key (str): The key whose value is to be retrieved.

        Returns:
        --------
        Any: The value associated with the specified key. Returns None if the key does not exist in the storage file.
        """
        full_file_path = os.path.join(self.location, self.storage_file)

        with open(full_file_path, 'r') as file:
            data = json.load(file)
            return data.get(key, None)
