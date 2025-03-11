"""
Defines the resources that comprise the speer-notes domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX
from . import notes
from . import users


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION,
    'notes': notes.DEFINITION,
    'users': users.DEFINITION    
}


DOMAIN_RELATIONS = {
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
