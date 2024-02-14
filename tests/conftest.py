import pytest
import requests


@pytest.fixture
def mock_requests():
    features = {}  # yeaaaa that is not so cool, but it is the quickest way to do it

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_post(*args, **kwargs):
        features = kwargs["json"]["features"]
        # check some other settings to restore feature state or add new features
        # features = update_features(features)
        return MockResponse(
            {"request_offset": 0.0, "features": features},
            200,
        )

    def mock_get(*args, **kwargs):
        return MockResponse({"features": features}, 200)

    requests.post = mock_post
    requests.get = mock_get
    return requests
