import pytest
from pytest_bdd import scenario
from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Deleting a single note is only successful when an authenticated user deletes her own note')
def test_authenticated_user_can_delete_a_single_note_that_they_had_previously_posted():
    pass

# all step definitions for this scenario are defined in a higher package
