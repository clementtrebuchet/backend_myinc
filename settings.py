# coding: utf8
"""

@Todo define use case

"""
from eve_app import BearerAuth

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
X_DOMAINS = 'http://localhost:8000,http://127.0.0.1:8000,'
X_HEADERS = ['Content-Type', 'Authorization', 'Access-Control-Allow-Origin:\'*\'']
X_EXPOSE_HEADERS = ['Content-Type', 'Authorization', 'Access-Control-Allow-Origin:\'*\'']
X_ALLOW_CREDENTIALS = True
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']
JSON = True

peoples = {

    # by default, the standard item entry point is defined as
    # '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },
    'public_methods': [],
    'public_item_methods': [],
    'allowed_roles': ['admin', 'user'],
    'allowed_item_roles': ['admin', 'user'],
    'allowed_read_roles': ['user'],
    'allowed_write_roles': ['admin', 'user'],
    'allowed_item_read_roles': ['user'],
    'allowed_item_write_roles': ['admin', 'user'],
    'authentication': BearerAuth,
    'allowed_filters': ['*'],
    'item_title': 'people',
    'resource_title': 'peoples',
    'projection': False,
    'sorting': True,
    'embedding': True,
    'embedded_fields': [''],
    'soft_delete': True,
    'pagination': True,
    'hateoas': True,
    'cache_control': '',
    'cache_expires': 3600 * 24,
    'versioning': True,

    'schema': {
        'firstname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 10,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
            # talk about hard constraints! For the purpose of the demo
            # 'lastname' is an API entry-point, so we need it to be unique.
            'unique': True,
        },

         'username': {
            'type': 'objectid',
            'required': True,
            # referential integrity constraint: value must exist in the
            # 'people' collection. Since we aren't declaring a 'field' key,
            # will default to `people._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'resource': 'eve.users',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
         },
        # 'role' is a list, and can only contain values from 'allowed'.
        'role': {
            'type': 'list',
            'allowed': ["admin", "freelancer", "recruiter"],
        },
        # An embedded 'strongly-typed' dictionary.
        'location': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'}
            },
        },

        'geoloc': {
            'type': 'point',

        },

        'born': {
            'type': 'datetime',
        }
    }
}
works = {
    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'owner'
    },
    'public_methods': ['GET', 'POST', 'PUT', 'DELETE'],
    'public_item_methods': ['GET','POST', 'PUT', 'DELETE'],
    'allowed_roles': ['admin', 'user'],
    'allowed_item_roles': ['admin', 'user'],
    'allowed_read_roles': ['user'],
    'allowed_write_roles': ['admin', 'user'],
    'allowed_item_read_roles': ['user'],
    'allowed_item_write_roles': ['admin', 'user'],
    'authentication': BearerAuth,
    'allowed_filters': ['*'],
    'item_title': 'work',
    'resource_title': 'works',
    'projection': False,
    'sorting': True,
    'embedding': True,
    'embedded_fields': [''],
    'soft_delete': True,
    'pagination': True,
    'hateoas': True,
    'versioning': True,
    'schema': {
        'title': {
            'type': 'string',
            'required': True,
        },
        'description': {
            'type': 'string',
        },
        'login': {
            'type': 'string',
        },
        'owner': {
            'type': 'objectid',
            'required': True,
            # referential integrity constraint: value must exist in the
            # 'people' collection. Since we aren't declaring a 'field' key,
            # will default to `people._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'resource': 'people',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
    }
}
DOMAIN = {'peoples': peoples,
          'works': works}
