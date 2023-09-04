import os
import random
import time
import uuid
from typing import Callable

# create a decorator method that will make a single request to given on __init__ server
import requests


class ClientHello:
    def __init__(self, ip: str, port: int, client_id: str, features: dict[str, bool]):
        self.ip = ip
        self.port = port
        self.client_id = client_id
        self.features = features


class PyFeature:
    def __init__(self, server: str):
        self.server = server
        self.features = {}
        self.request_offset = 0
        self.last_request_time = 0
        unique_sep = "||"
        self._id = str(uuid.uuid5(
            uuid.NAMESPACE_X500,
            os.environ.get("CI", str(random.random())) + unique_sep + os.environ.get("CI2", str(random.random()))))
        # self.__make_first_request()

    def __make_first_request(self):
        params = {
            "ip": "localhost",
            "port": 8080,
            "client_id": self._id,
            "features": self.features,
        }
        response = requests.post(self.server + "/hello", json=params)
        response_model = response.json()
        self.request_offset = response_model["request_offset"]
        self.last_request_time = time.time()

    def feat(self, feature_name: str | None = None, feature_status: bool = True) -> Callable:
        def decorator(func):
            def wrapper(*args, **kwargs):
                print("I am wrapper")
                if self.last_request_time == 0:
                    self.__make_first_request()
                elif self.last_request_time + self.request_offset < time.time():
                    self.__check_config_update()
                return func(*args, **kwargs)

            print("I am decorator")
            if feature_name not in self.features:
                self.features.update({feature_name: feature_status})
            return wrapper
        return decorator

    def __check_config_update(self):
        response = requests.get(self.server + f"/{self._id}/config")
        print(response.json())


# at the moment decorators collecting cool info about all functions and I can set up all features
# but how to use each decorator before call of function also?

feature = PyFeature("http://127.0.0.1:8080")


@feature.feat(feature_name="feature_1")
def get_data():
    print("1 I am getting data")


@feature.feat(feature_name="feature_2")
def get_data_2():
    print("2 I am getting data")


if __name__ == "__main__":
    get_data()
    get_data()
