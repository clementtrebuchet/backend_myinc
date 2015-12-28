# coding: utf8
# @Todo define use case
"""
12/26/15 5:36 PM


"""

__author__ = 'clement'
# coding: utf8

"""
12/17/15 10:35 PM
model definition for peoples  document

"""
from security.bearer_auth import BoAuth

__author__ = 'clement'


def users():
    """
     by default, the standard item entry point is defined as
    '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    additional read-only entry point. This way consumers can also perform
    GET requests at '/people/<lastname>'.
    :return:  schema

    """
    users = {

        'additional_lookup': {
            'url': 'regex("[\w]+")',
            'field': 'username'
        },
        'public_methods': [''],
        'public_item_methods': [''],
        'allowed_roles': ['admin'],
        'allowed_item_roles': ['admin'],
        'allowed_read_roles': ['admin'],
        'allowed_write_roles': ['admin'],
        'allowed_item_read_roles': ['admin'],
        'allowed_item_write_roles': ['admin'],
        'authentication': BoAuth,
        'allowed_filters': ['*'],
        'item_title': 'user',
        'resource_title': 'users',
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

            "username": {'type': "string"},
            "hashpw": {'type': "string"},

        }

    }
    return users
