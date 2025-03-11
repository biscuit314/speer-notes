import logging
from datetime import datetime, timezone
import hashlib
import pymongo
import pytest
from pymongo import MongoClient
from hypermea_service import HypermeaService  # your existing class
from __tests__ import ADMIN_CREDENTIALS

import os

LOG = logging.getLogger('pytest')

logger = logging.getLogger()
handler = [x for x in logger.handlers if x.name == 'console'][0]
handler.setLevel(getattr(logging, 'WARNING'))

os.environ['HY_URL_PREFIX'] = 'api'
os.environ['HY_API_PORT'] = '2113'
os.environ['REDIS_DB'] = '1'

os.environ['HY_MONGO_DBNAME'] = 'pytest'
os.environ['HY_TRACE_LOGGING'] = 'Disabled'
os.environ['HY_CACHE_CONTROL'] = 'no-cache, no-store, must-revalidate'
os.environ['HY_CACHE_EXPIRES'] = '30'
os.environ['HY_DISABLE_RFC6861'] = 'Yes'
os.environ['HY_DISABLE_HYPERMEDIA'] = 'Yes'
# os.environ['HY_RATE_LIMIT'] = '(10, 15)'


def get_sysop_user():
    username, password = ADMIN_CREDENTIALS
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')

    return {
        'username': username,
        'name': 'System Administrator',
        'password': hashlib.sha256(f'{username}:{password}'.encode('utf8')).hexdigest(),
        'isAdmin': True,
        '_etag': '1cbd3a75c6ce518dac192a9c5280e78064dfa8ca',
        '_created': now,
        '_updated': now
    }


@pytest.fixture
def api():
    service = HypermeaService(host='0.0.0.0', debug='Enabled')
    app = service._app

    def setup_database():
        sysop = get_sysop_user()
        client = MongoClient(
            app.config.get('MONGO_HOST'), app.config.get('MONGO_PORT')
        )
        db = client[app.config.get('MONGO_DBNAME')]
        db.users.insert_one(sysop)

        index_name = 'TitleBodyTextIndex'

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

        client.close()

    def cleanup_database():
        connection = MongoClient(
            app.config.get('MONGO_HOST'), app.config.get('MONGO_PORT')
        )
        connection.drop_database(app.config.get('MONGO_DBNAME'))
        connection.close()

    cleanup_database()
    setup_database()
    yield app.test_client()
    cleanup_database()
