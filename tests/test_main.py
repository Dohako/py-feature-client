from main import PyFeature
from models import Behaviour


def test_decorator(mock_requests):
    server = "http://localhost:8080"
    feature = PyFeature(server)

    @feature.feat()
    def test_func():
        return "Hello"

    assert test_func() == "Hello"
    assert feature.features == {"test_func": (True, Behaviour.RETURN_NONE)}

    @feature.feat("test_feature")
    def test_func2():
        return "Hello"

    assert test_func2() == "Hello"
    assert feature.features == {
        "test_func": (True, Behaviour.RETURN_NONE),
        "test_feature": (True, Behaviour.RETURN_NONE),
    }

    @feature.feat("test_feature_2", False)
    def test_func3():
        return "Hello"

    assert test_func3() == None
    assert feature.features == {
        "test_func": (True, Behaviour.RETURN_NONE),
        "test_feature": (True, Behaviour.RETURN_NONE),
        "test_feature_2": (False, Behaviour.RETURN_NONE),
    }

    feature.features["test_feature"] = (False, Behaviour.RETURN_NONE)
    # this test will fail on long enough time, because of the request offset
    # and thus because I can't by design change feature state inside client app
    # it is fine to fail
    assert test_func2() == None
    assert feature.features == {
        "test_func": (True, Behaviour.RETURN_NONE),
        "test_feature": (False, Behaviour.RETURN_NONE),
        "test_feature_2": (False, Behaviour.RETURN_NONE),
    }
