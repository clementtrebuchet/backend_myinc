# coding: utf8

"""
12/17/15 10:35 PM
model definition for peoples  document

"""
from security.bearer_auth import BoAuth

__author__ = 'clement'


def promotions():
    """
     by default, the standard item entry point is defined as
    '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    additional read-only entry point. This way consumers can also perform
    GET requests at '/people/<lastname>'.
    :return:  schema

    """

    promotions = {

        'additional_lookup': {
            'url': 'regex("[\w]+")',
            'field': 'title'
        },
        'public_methods': ['GET'],
        'public_item_methods': ['GET'],
        'allowed_roles': ['admin'],
        'allowed_item_roles': ['admin'],
        'allowed_read_roles': ['user'],
        'allowed_write_roles': ['admin'],
        'allowed_item_read_roles': ['user'],
        'allowed_item_write_roles': ['admin'],
        'authentication': BoAuth,
        'allowed_filters': ['*'],
        'item_title': 'promotion',
        'resource_title': 'promotions',
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
            'title': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 20,
                'required': True,
                'unique': True,
            },
            'description': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 350,
            },

        },
        # 'role' is a list, and can only contain values from 'allowed'.
        'role': {
            'type': 'list',
            'allowed': ["admin"],
        },
    }
    return promotions
