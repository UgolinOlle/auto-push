import json
import os
from typing import Any, Dict

import requests
from requests.auth import HTTPBasicAuth


class Github:
    """
    A class to interact with the Github API for managing user profile information and issues.

    This class encapsulates methods for updating the biography and status of a Github user's profile and for creating issues in a specified repository. It handles authentication and provides a simplified interface for making specific Github API calls.

    Attributes:
    -----------
    username (str): Github username used for authentication.
    base_url (str): Base URL for the Github API.
    base_grapql_url (str): Base URL for the Github GraphQL API.
    auth (HTTPBasicAuth): Authentication object with credentials.

    Methods:
    --------
    update_bio(content): Updates the biography of the Github user's profile.
    update_status(content): Updates the status of the Github user's profile.
    create_issue(title, body, labels): Creates a new issue in a specified repository.
    """

    def __init__(self) -> None:
        """
        Initializes the Github object with authentication details.

        Sets up the authentication credentials for accessing the Github API using a personal access token stored in environment variables. Configures the base URLs for standard and GraphQL API endpoints.
        """
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

        Sends a PATCH request to the Github API to update the biography section of the user's profile.

        Parameters:
        -----------
        content (str): The new biography content to be set.

        Returns:
        --------
        Dict[str, Any]: The JSON response from the Github API.

        Raises:
        -------
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

        Sends a POST request to the Github GraphQL API to update the user's status message.

        Parameters:
        -----------
        content (str): The new status message to be set.

        Returns:
        --------
        Dict[str, Any]: The JSON response from the Github GraphQL API.

        Raises:
        -------
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

    def create_issue(self, title: str, body: str, labels: list = []) -> Dict[str, Any]:
        """
        Creates a new issue in the specified repository.

        Sends a POST request to the Github API to create a new issue in the 'ugolinolle/auto-push' repository.

        Parameters:
        -----------
        title (str): The title of the issue.
        body (str): The detailed description of the issue.
        labels (list): A list of labels to attach to the issue.

        Returns:
        --------
        Dict[str, Any]: The JSON response from the Github API.

        Raises:
        -------
        requests.HTTPError: If the HTTP request results in an unsuccessful status code.
        """
        url = f"{self.base_url}/repos/ugolinolle/auto-push/issues"
        data = {
            "title": title,
            "body": body,
            "labels": labels
        }
        response = requests.post(
            url, auth=self.auth, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()
