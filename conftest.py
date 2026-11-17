import pytest
import requests

from Config import BASE_URL, TOKEN
from utils.loggers import get_logger

logger = get_logger(__name__)


@pytest.fixture
def api_client():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {TOKEN}"
    })

    logger.info("API client initialized")#logs the informational message indicating that the api client is initialized


    original_request = session.request

    def logged_request(method, url, **kwargs):
        logger.info(f"{method} {url}")

        response = original_request(method, url, **kwargs)

        logger.info(f"Response status: {response.status_code}")
        return response

    session.request = logged_request

    return session


@pytest.fixture
def candidate_id(api_client):
    url = f"{BASE_URL}/api/v2/recruitment/candidates"

    payload = {
        "firstName": "API",
        "lastName": "TestCandidate",
        "email": "api.testcandidate@example.com"
    }

    response = api_client.post(url, json=payload)

    assert response.status_code == 200

    candidate_id = response.json()["data"]["id"]

    yield candidate_id

    # Cleanup only if the candidate still exists
    get_url = f"{BASE_URL}/api/v2/recruitment/candidates/{candidate_id}"
    get_response = api_client.get(get_url)

    if get_response.status_code == 200:
        api_client.delete(
            url,
            json={"ids": [candidate_id]}
        )