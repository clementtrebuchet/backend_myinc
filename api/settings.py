# coding: utf8
"""
Eve settings files

"""
from models.onions import onions
from models.peoples import peoples
from models.promotion import promotions
from models.users import users
from models.skills import skills

__author__ = 'clement'
SENTINEL_MONGO_HOST = 'localhost'
SENTINEL_MONGO_PORT = 27017
# MONGO_USERNAME = 'user'
# MONGO_PASSWORD = 'user'
SENTINEL_MONGO_DBNAME = 'eve'
SENTINEL_REDIS_URL = 'redis://localhost:6379/0'
# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['POST', 'GET', 'DELETE']
# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET','PUT', 'PATCH', 'DELETE']
# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20
X_DOMAINS = 'http://localhost:8000,http://127.0.0.1:8000, https://localhost:8000, https://127.0.0.1:8000,'
X_HEADERS = ['Content-Type', 'Access-Control-Allow-Headers', 'Authorization', 'X-Requested-With', 'If-Match']
X_EXPOSE_HEADERS = ['Content-Type', 'Access-Control-Allow-Headers', 'Authorization', 'X-Requested-With', 'If-Match']
X_ALLOW_CREDENTIALS = True
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'  # ("04/21/15 20:56:16")
MONGO_QUERY_BLACKLIST = ['$where']
# API_VERSION = 'v1'
# URL_PREFIX = 'api'
JSON = True
XML =False
SWAGGER = {
    'info': {
        'title': 'DevOps Open Consulting API',
        'version': '1.0',
        'description': 'Presentation API',
        'termsOfService': 'public use',
        'contact': {
            'name': 'GEEK CONSULTING',
            'email': 'clement.trebuchet@gmail.com'
        },
        'license': {
            'name': 'bsd',
            'url': 'https://curriculum.trebuchetclement.fr',
        }
    },
    'host': 'curriculum.trebuchetclement.fr:5055'
}
DOMAIN = {
    'peoples': peoples(),
    'skills': skills(),
    'promotions': promotions(),
    'users': users(),
    'onions': onions()
}
