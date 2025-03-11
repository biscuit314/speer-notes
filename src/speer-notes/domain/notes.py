"""
Defines the notes resource.
"""
from domain._common import COMMON_FIELDS


SCHEMA = {
    'title': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'body': {
        'type': 'string'
    },
    '_owner': {
        'type': 'string',
        'readonly': True
    },
    '_shared_with': {
        'type': 'list',
        'schema': {'type': 'string'}
    },

}


DEFINITION = {
    'schema': SCHEMA,
    'datasource': {
        'projection': {'_owner': 0, '_shared_with': 0}
    }
}
