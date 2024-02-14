import pytest
import requests


@pytest.fixture
def mock_requests():
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_post(*args, **kwargs):
        return MockResponse({"request_offset": 0.0}, 200)

    def mock_get(*args, **kwargs):
        return MockResponse({"feature1": True, "feature2": False}, 200)

    requests.post = mock_post
    requests.get = mock_get
    return requests
