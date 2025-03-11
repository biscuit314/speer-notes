import pytest
from pytest_bdd import scenario

from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Authenticated users see only their own list of notes')
def test_authenticated_users_see_only_their_own_list_of_notes():
    pass


# Given a user named alice is signed up

# And a user named bob is signed up

# And alice has added notes

# And bob has added notes

# When alice requests all notes

@then(parsers.parse('the response contains only the notes {username} added'))
def step_impl(context, username):
    notes_to_add = context[username]['notes_to_add']
    notes_fetched =  [{'title': note['title'], 'body': note['body']} for note in context[username]['notes_fetched']]

    assert_that(context[username]['status_code']).is_equal_to(200)
    assert_that(len(notes_fetched)).is_equal_to(len(notes_to_add))
    assert_that(notes_fetched).contains_only(*notes_to_add)
