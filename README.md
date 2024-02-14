# py-feature-client

This is a Python client for the [FeatureServer]()

## Description

This is simple and straightforward version of Feature flag management system.

Two ways of feature creation:

1. Using the list in your code
2. Automatically by script, but names would be given unique, but based on some surrounding function or class name.

Features are set from the server and are cached for 5 minutes. After that time,
new request is made to the server to get new features, but only when needed. That means that no polling inside the
client is done.

Also, that means that feature would be updated only at least 5 minutes after it was changed on the server.

## Usage

You can use decorator or direct method call to check if feature is active and do whatever you want.

```python
from feature_client import FeatureClient

client = FeatureClient('http://localhost:8000', feature_list=['feature_name'])

if client.is_active('feature_name'):
    print('Feature is active')
else:
    print('Feature is not active')


@client.feature('feature_name')
def feature():
    print('Feature is active')


feature()


@client.feature
def feature_2():
    print('Feature 2 is active')


feature_2()
```
