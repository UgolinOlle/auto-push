import os
import requests
from typing import Dict, Any


class Weather:
    """
    A class to fetch weather information for a specific location using the Weather API.

    Attributes:
        location (str): The location for which to fetch the weather. Defaults to "Bangkok".
        base_url (str): The base URL for the Weather API.
        api_key (str): The API key for authenticating with the Weather API, read from the environment.
        url (str): The full URL to make the API request.

    Methods:
        get_weather: Retrieves the current weather data for the location.
    """

    def __init__(self) -> None:
        """
        Initializes the Weather object by constructing the request URL.
        """
        self.location: str = "Bangkok"
        self.base_url: str = "https://api.weatherapi.com/v1"
        self.api_key: str = os.getenv("WEATHER_API_KEY")
        self.url: str = f"{self.base_url}/current.json?key={self.api_key}&q={self.location}&aqi=no"

    def get_weather(self) -> Dict[str, Any]:
        """
        Fetches the current weather data from the Weather API for the specified location.

        Returns:
            Dict[str, Any]: A dictionary containing the current weather data.

        Raises:
            requests.RequestException: An error occurred during the API request.
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
        Formats the weather data.

        Parameters:
            weather_data (dict): A dictionary containing weather data.

        Returns:
            str: A formatted string with weather details and emojis.
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
