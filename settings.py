# coding: utf8
"""
Eve settings files

"""

from models.peoples import peoples
from models.works import works

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
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']
# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20
X_DOMAINS = 'http://localhost:8000,http://127.0.0.1:8000, https://localhost:8000, https://127.0.0.1:8000,'
X_HEADERS = ['Content-Type', 'Authorization', 'Access-Control-Allow-Origin:\'*\'']
X_EXPOSE_HEADERS = ['Content-Type', 'Authorization', 'Access-Control-Allow-Origin:\'*\'']
X_ALLOW_CREDENTIALS = True
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']
JSON = True

DOMAIN = {'peoples': peoples,
          'works': works}
