import pytest
from pytest_bdd import scenario
from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Updating a single note is only successful when an authenticated user updates her own note')
def test_authenticated_user_can_update_a_single_note_that_they_had_previously_posted(context):
    pass

# all step definitions for this scenario are defined in a higher package
