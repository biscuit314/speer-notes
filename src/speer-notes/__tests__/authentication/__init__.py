import json
from pytest_bdd import scenario, when, then
from __tests__ import *

FEATURE_PATH = 'authentication.feature'

@then('the attempt fails')
def step_impl(api, context):
    assert_that(context['response']).is_equal_to(401)