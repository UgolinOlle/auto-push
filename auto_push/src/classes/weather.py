import os
import requests
from typing import Dict, Any


class Weather:
    """
    A class for fetching and formatting weather information from the Weather API.

    This class provides functionality to retrieve current weather data for a specified location and format it for display or further use.

    Attributes:
    -----------
    location (str): The location for which to fetch the weather, defaulting to "Bangkok".
    base_url (str): The base URL of the Weather API.
    api_key (str): The API key for authenticating with the Weather API, obtained from environment variables.
    url (str): The complete URL for making the API request, constructed using the base URL, API key, and location.

    Methods:
    --------
    get_weather(): Retrieves the current weather data for the specified location.
    format_weather(data): Formats the retrieved weather data into a readable string.
    """

    def __init__(self) -> None:
        """
        Initializes the Weather instance with default values and constructs the API request URL.

        Sets the default location to "Bangkok", fetches the API key from environment variables, and constructs the full URL for API requests. The URL includes parameters for the location and air quality index.
        """
        self.location: str = "Bangkok"
        self.base_url: str = "https://api.weatherapi.com/v1"
        self.api_key: str = os.getenv("WEATHER_API_KEY")
        self.url: str = f"{
            self.base_url}/current.json?key={self.api_key}&q={self.location}&aqi=no"

    def get_weather(self) -> Dict[str, Any]:
        """
        Fetches the current weather data from the Weather API for the specified location.

        Sends a GET request to the Weather API and returns the current weather data as a dictionary. Handles HTTP errors and other exceptions by raising a RequestException.

        Returns:
        --------
        Dict[str, Any]: A dictionary containing the current weather data, including temperature, conditions, and other relevant details.

        Raises:
        -------
        requests.RequestException: If an HTTP error or other exception occurs during the API request.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            raise requests.RequestException(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise requests.RequestException(f"An error occurred: {err}")

    def format_weather(self, data: Dict) -> str:
        """
        Formats the weather data into a human-readable string.

        Takes a dictionary containing weather data and formats it, providing details such as location, temperature, and weather conditions.

        Parameters:
        -----------
        data (Dict): A dictionary containing weather data.

        Returns:
        --------
        str: A formatted string presenting key weather information in a readable format.
        """
        condition = data.get('current', {}).get(
            'condition', {}).get('text', 'Not available')
        temp_c = data.get('current', {}).get('temp_c', 'N/A')

        formatted_weather = (
            f"Location: {data.get('location', {}).get('name', 'Unknown')} | "
            f"Temperature: {temp_c}°C | "
            f"Condition: {condition}"
        )

        return formatted_weather
