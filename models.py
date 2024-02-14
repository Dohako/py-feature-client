from enum import Enum


class Behaviour(Enum):
    """
    Enum to define the behaviour of the feature
    """

    RAISE_ERROR = "RAISE_ERROR"
    RETURN_NONE = "RETURN_NONE"
    RETURN_DEFAULT = "RETURN_DEFAULT"
