import os
import requests
import json
from requests.auth import HTTPBasicAuth
from typing import Any, Dict


class Github:
    """
    A class to interact with the Github API for updating user profile information.

    This class provides methods to update the biography and status of a Github user's profile.
    It also monitors keyboard activity to set the user's status accordingly.

    Attributes:
        username (str): Github username for authentication.
        base_url (str): Base URL for the Github API.
        base_grapql_url (str): Base URL for the Github GraphQL API.
        auth (HTTPBasicAuth): Authentication object with credentials.
    """

    def __init__(self) -> None:
        """
        Initializes the Github object with authentication details and starts keyboard activity monitoring.
        """
        # API configuration
        self.username: str = "ugolinolle"
        self.base_url: str = "https://api.github.com"
        self.base_grapql_url: str = "https://api.github.com/graphql"
        self.auth: HTTPBasicAuth = HTTPBasicAuth(
            self.username, os.getenv("GITHUB_PERSONAL_ACCESS", "default_token"))
        self.headers = {
            'Authorization': f'bearer {os.getenv("GITHUB_PERSONAL_ACCESS", "default_token")}',
            'Content-Type': 'application/json'
        }

    def update_bio(self, content: str) -> Dict[str, Any]:
        """
        Updates the biography of the Github user's profile.

        Parameters:
            content (str): The new biography content to be set.

        Returns:
            Dict[str, Any]: The JSON response from the Github API.

        Raises:
            requests.HTTPError: If the HTTP request results in an unsuccessful status code.
        """
        headers = {'Content-Type': 'application/json'}
        data = {'bio': content}
        response = requests.patch(url=f"{self.base_url}/user",
                                  auth=self.auth, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return response.json()

    def update_status(self, content: str) -> Dict[str, Any]:
        """
        Updates the status of the Github user's profile.

        Parameters:
            content (str): The new status message to be set.

        Returns:
            Dict[str, Any]: The JSON response from the Github GraphQL API.

        Raises:
            requests.HTTPError: If the HTTP request results in an unsuccessful status code.
        """
        query = """
            mutation {
                changeUserStatus(input: {clientMutationId: "ugoline", emoji: ":computer:", limitedAvailability: false,  message: "%s"}) {
                    clientMutationId
                    status {
                        message
                        emoji
                    }
                }
            }
        """ % content
        response = requests.post(url=self.base_grapql_url, json={
            "query": query}, headers=self.headers)
        response.raise_for_status()
        return response.json()
