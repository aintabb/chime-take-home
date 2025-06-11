import pytest
import logging
from src.joke_api import JokeAPIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    """Create a JokeAPIClient instance for testing."""
    return JokeAPIClient()


def test_single_programming_joke(client):
    """
    Test that a single random programming joke is returned with correct type and structure.

    This test verifies:
    - API returns a successful response
    - Response contains exactly one joke
    - Joke has the correct type and structure
    - All required fields are present and valid
    """
    logger.info("Testing single programming joke endpoint")
    jokes = client.get_random_joke()

    assert isinstance(jokes, list), "Response should be a list"
    assert len(jokes) == 1, "Should return exactly one joke"
    client.validate_joke_structure(jokes[0])
    logger.info("Single programming joke test passed")


def test_ten_programming_jokes(client):
    """
    Test that exactly 10 programming jokes are returned.

    This test verifies:
    - API returns a successful response
    - Response contains exactly 10 jokes
    - All jokes have the correct structure and type
    """
    logger.info("Testing ten programming jokes endpoint")
    jokes = client.get_ten_jokes()

    assert isinstance(jokes, list), "Response should be a list"
    assert len(jokes) == 10, "Should return exactly 10 jokes"

    for joke in jokes:
        client.validate_joke_structure(joke)

    logger.info("Ten programming jokes test passed")
