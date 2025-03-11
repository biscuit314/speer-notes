#! /usr/bin/env python3

from datetime import datetime, timezone
import hashlib
import pymongo

client = pymongo.MongoClient()
db = client['speer-notes']

now = datetime.now(timezone.utc)

username = 'sysop'
password = 'swordfish'

db.users.insert_one({
    'username': username,
    'name': 'System Administrator',
    'password': hashlib.sha256(f'{username}:{password}'.encode('utf8')).hexdigest(),
    'isAdmin': True,
    '_etag': '1cbd3a75c6ce518dac192a9c5280e78064dfa8ca',
    '_created': now,
    '_updated': now
})
