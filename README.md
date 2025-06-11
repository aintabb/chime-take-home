# Joke Factory API Test Suite

This test suite verifies the functionality of the Joke Factory API, specifically focusing on programming jokes endpoints.

## Features

- Tests single random programming joke endpoint
- Tests ten programming jokes endpoint
- Validates joke structure and content
- Includes error handling and logging
- Checks for duplicate jokes

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/aintabb/chime-take-home.git
cd chime-take-home
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

To run all tests:
```bash
pytest tests/test_joke_api.py -v
```

To run tests with detailed logging:
```bash
pytest tests/test_joke_api.py -v --log-cli-level=INFO
```

## Test Structure

The test suite includes:

1. `test_single_programming_joke`: Verifies the `/random` endpoint
   - Checks response structure
   - Validates joke type is "programming"
   - Ensures all required fields are present

2. `test_ten_programming_jokes`: Verifies the `/ten` endpoint
   - Confirms exactly 10 jokes are returned
   - Validates structure of each joke
   - Ensures all jokes are of type "programming"
