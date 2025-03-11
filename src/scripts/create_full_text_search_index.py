#! /usr/bin/env python3

import pymongo
from pymongo.errors import OperationFailure

client = pymongo.MongoClient()
db = client['speer-notes']

index_name = 'TitleBodyTextIndex'

try:
    db.notes.drop_index(index_name)
except OperationFailure:
    pass  # no need to drop an index that doesn't exist

db.notes.create_index(
    [
        ('title', pymongo.TEXT),
        ('body', pymongo.TEXT)
    ], 
    weights={
        'title': 3,
        'body': 2
    },
    name=index_name, 
    default_language='english'
)
