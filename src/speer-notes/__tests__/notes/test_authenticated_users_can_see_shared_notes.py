import pytest
from pytest_bdd import scenario
from __tests__.notes import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Authenticated user can see notes posted by others shared with her')
def test_authenticated_users_can_see_shared_notes():
    pass

"""
  Scenario: Authenticated user can see notes posted by others shared with her
    Given a user named alice is signed up
      And a user named bob is signed up
      And someone named mallory who is not signed up
      And alice adds notes
        | title        | body         |
        | Alice note 1 | Alice body 1 |
      And bob adds notes
        | title      | body       |
        | Bob note 1 | Bob body 1 |
      When alice shares a single note with bob that alice added
      And bob requests all notes
      Then...>
"""

@then(parsers.parse('the result is all notes added by {username} plus the one that was shared by {sharer}'))
def step_impl(context, username, sharer):
    notes_added = context[username]['notes_added']
    notes_fetched = context[username]['notes_fetched']
    shared_note_id = context[sharer]['shared_note_id']
    assert_that(len(notes_fetched)).is_equal_to(len(notes_added) + 1)
    assert_that(any(note['_id'] == shared_note_id for note in notes_fetched)).is_true()
