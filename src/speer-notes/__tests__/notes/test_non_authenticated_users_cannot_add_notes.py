import pytest
from pytest_bdd import scenario

from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Non-authenticated users cannot add notes')
def test_non_authenticated_users_cannot_add_notes():
    pass

# Given someone named mallory who is not signed up

# When mallory has added notes

@then('the notes are not added')
def step_impl(context):
    all_codes = list(set(context['mallory']['status_codes']))
    first_code = all_codes[0]

    assert_that(len(all_codes)).is_equal_to(1)
    assert_that(first_code).is_equal_to(401)
