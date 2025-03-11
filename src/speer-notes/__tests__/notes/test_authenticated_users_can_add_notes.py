import pytest
from pytest_bdd import scenario
from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Authenticated users can add notes')
def test_authenticated_users_can_add_notes():
    pass

# Given a user is named alice is signed up

# When alice has added notes

@then('the notes are added')
def step_impl(context):
    all_codes = list(set(context['alice']['status_codes']))
    first_code = all_codes[0]

    assert_that(len(all_codes)).is_equal_to(1)
    assert_that(first_code).is_equal_to(201)
    assert_that(len(context['alice']['status_codes'])).is_equal_to(len(context['alice']['notes_to_add']))
