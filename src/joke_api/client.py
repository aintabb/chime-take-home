import logging
import time
from typing import Dict, List
import requests
from requests.exceptions import RequestException

from .exceptions import JokeAPIError

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
RANDOM_JOKE_URL = "https://official-joke-api.onrender.com/jokes/programming/random"
TEN_JOKES_URL = "https://official-joke-api.onrender.com/jokes/programming/ten"
TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
EXPECTED_JOKE_KEYS = {"id", "type", "setup", "punchline"}
EXPECTED_JOKE_TYPE_PROGRAMMING = "programming"


class JokeAPIClient:
    """Client for interacting with the Joke API."""

    def __init__(
        self,
        timeout: int = TIMEOUT,
        max_retries: int = MAX_RETRIES,
        retry_delay: int = RETRY_DELAY,
    ):
        """
        Initialize the Joke API client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _make_request(self, url: str, retry_count: int = 0) -> List[Dict]:
        """
        Make a request to the Joke API with error handling and retry logic.

        Args:
            url: Full URL to call
            retry_count: Current retry attempt number

        Returns:
            List[Dict]: List of jokes from the API

        Raises:
            JokeAPIError: If the request fails after all retries
        """
        try:
            logger.info(
                f"Making API request to {url} (attempt {retry_count + 1}/{self.max_retries + 1})"
            )
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if retry_count < self.max_retries:
                logger.warning(
                    f"Request failed: {str(e)}. Retrying in {self.retry_delay} seconds..."
                )
                time.sleep(self.retry_delay)
                return self._make_request(url, retry_count + 1)
            logger.error(
                f"API request failed after {self.max_retries + 1} attempts: {str(e)}"
            )
            raise JokeAPIError(
                f"Failed to fetch jokes after {self.max_retries + 1} attempts: {str(e)}"
            )

    def get_random_joke(self) -> List[Dict]:
        """
        Get a random programming joke.

        Returns:
            List[Dict]: List containing a single random joke
        """
        return self._make_request(RANDOM_JOKE_URL)

    def get_ten_jokes(self) -> List[Dict]:
        """
        Get ten programming jokes.

        Returns:
            List[Dict]: List of ten programming jokes
        """
        return self._make_request(TEN_JOKES_URL)

    @staticmethod
    def validate_joke_structure(joke: Dict) -> None:
        """
        Validate the structure of a single joke.

        Args:
            joke: Dictionary containing joke data

        Raises:
            AssertionError: If joke structure is invalid
        """
        assert isinstance(joke, dict), "Joke should be a dictionary"
        assert all(
            key in joke for key in EXPECTED_JOKE_KEYS
        ), "Joke missing required fields"
        assert (
            joke["type"] == EXPECTED_JOKE_TYPE_PROGRAMMING
        ), "Joke type should be 'programming'"

        # Extra checks. They might not necessary
        assert isinstance(joke["setup"], str), "Setup should be a string"
        assert isinstance(joke["punchline"], str), "Punchline should be a string"
        assert len(joke["setup"]) > 0, "Setup should not be empty"
        assert len(joke["punchline"]) > 0, "Punchline should not be empty"
