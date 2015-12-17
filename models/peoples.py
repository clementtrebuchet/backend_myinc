# coding: utf8

"""
12/17/15 10:35 PM
model definition for peoples  document

"""
from api.version_1 import BoAuth

__author__ = 'clement'

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
    'authentication': BoAuth,
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