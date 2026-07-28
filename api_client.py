"""
API Client module for AskBia platform.
Provides a client wrapper to interface with AskBia back-end services.
"""

import logging
import requests

logger = logging.getLogger(__name__)

class AskBiaAPIClient:
    """
    Client for interacting with the AskBia API.
    Handles user queries, authentication, and location lookups.
    """

    def __init__(self, base_url: str, api_key: str = None):
        """
        Initialize the API client.

        :param base_url: Base URL of the AskBia API server.
        :param api_key: Optional API key for authenticating requests.
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def ask_query(self, query_text: str) -> dict:
        """
        Send a natural language query to the AskBia AI helper.

        :param query_text: Text query representing the user's question.
        :return: API response payload as a dictionary.
        """
        url = f"{self.base_url}/query"
        payload = {"query": query_text}
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying AskBia API: {e}")
            return {"success": False, "error": str(e)}

    def get_locations(self) -> list:
        """
        Retrieve list of available service locations for AskBia.

        :return: List of location dictionaries.
        """
        url = f"{self.base_url}/locations"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching locations: {e}")
            return []

if __name__ == "__main__":
    # Client usage example
    logging.basicConfig(level=logging.INFO)
    client = AskBiaAPIClient("https://api.askbia.example.com")
    print("AskBia API Client initialized.")
