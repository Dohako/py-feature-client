import os
import random
import time
import uuid
import warnings
from typing import Callable, Any

import requests

from models import Behaviour


class PyFeature:
    def __init__(self, server: str) -> None:
        self.server = server
        self.features: dict[str, tuple[bool, Behaviour]] = {}
        self.request_offset = 0.0
        self.last_request_time = 0.0
        unique_sep = "||"
        self._id = str(
            uuid.uuid5(
                uuid.NAMESPACE_X500,
                os.environ.get("CI", str(random.random()))
                + unique_sep
                + os.environ.get("CI2", str(random.random())),
            )
        )

    def __make_first_request(self) -> None:
        """
        Make first request to server to get request offset and first feature list
        :return:
        """
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

    def __check_config_update(self):
        response = requests.get(self.server + f"/{self._id}/config")
        print(response.json())

    def __empty_func(self, *args: Any, **kwargs: Any) -> None:
        warnings.warn("Feature is disabled", UserWarning)

    def feat(
            self,
            feature_name: str | None = None,
            feature_status: bool = True,
            behaviour: Behaviour = Behaviour.RETURN_NONE,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            def wrapper(*args: Any, **kwargs: Any) -> Callable:
                if self.last_request_time == 0:
                    self.__make_first_request()
                elif self.last_request_time + self.request_offset < time.time():
                    self.__check_config_update()
                if not feature_status and behaviour == Behaviour.RETURN_NONE:
                    return self.__empty_func(*args, **kwargs)  # type: ignore
                elif not feature_status and behaviour == Behaviour.RAISE_ERROR:
                    raise ValueError("Feature is disabled")
                return func(*args, **kwargs)

            if feature_name and feature_name not in self.features:
                self.features.update({feature_name: (feature_status, behaviour)})
            elif func.__name__ not in self.features:
                self.features.update({func.__name__: (feature_status, behaviour)})
            return wrapper

        return decorator
