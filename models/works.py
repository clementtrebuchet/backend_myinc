# coding: utf8
"""
12/17/15 10:33 PM
model definition for peoples works document

"""
from api.version_1 import BoAuth

__author__ = 'clement'

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
    'authentication': BoAuth,
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