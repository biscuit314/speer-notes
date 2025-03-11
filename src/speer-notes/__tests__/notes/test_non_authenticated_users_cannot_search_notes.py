import pytest
from pytest_bdd import scenario
from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Non-authenticated user cannot search for notes')
def test_non_authenticated_users_cannot_search_notes():
    pass

# all step definitions for this scenario are defined in a higher package
