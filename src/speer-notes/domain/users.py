"""
Defines the users resource.
"""

SCHEMA = {
    'username': {
        'type': 'string',
        'required': True,
        'empty': False,
        'unique': True
    },
    'name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'password': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'isAdmin': {
        'type': 'boolean',
        'required': True,
        'default': False
    }
}

DEFINITION = {
    'schema': SCHEMA,
    'datasource': {
        'projection': {'password': 0}
    },
    'additional_lookup': {
        'url': r'regex("[\w]+")',
        'field': 'username'
    },
    'allowed_roles': ['admin']
}
