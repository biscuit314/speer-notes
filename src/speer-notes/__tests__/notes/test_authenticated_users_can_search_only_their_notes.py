import pytest
from pytest_bdd import scenario
from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, "Authenticated user's search results do not include matching notes posted by others")
def test_authenticated_users_can_search_only_their_notes():
    pass

# all step definitions for this scenario are defined in a higher package
