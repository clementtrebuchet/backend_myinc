# coding: utf8
"""

"""

__author__ = 'clement.trebuchet@gmail.com'

from security.bearer_auth import BoAuth


def onions_exits():
    """

    :return:skills schema
    """
    onions_exits = {
        'cache_control': 'max-age=10,must-revalidate',
        'cache_expires': 10,
        'additional_lookup': {
            'url': 'regex("\w+\.\w+")',
            'field': 'hiddenService'
        },
        'public_methods': ['GET'],
        'public_item_methods': ['GET'],
        'allowed_roles': ['admin', 'user'],
        'allowed_item_roles': ['admin', 'user'],
        'allowed_read_roles': ['user'],
        'allowed_write_roles': ['admin', 'user'],
        'allowed_item_read_roles': ['user'],
        'allowed_item_write_roles': ['admin', 'user'],
        'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
        'resource_methods': ['POST', 'GET', 'DELETE'],
        'authentication': BoAuth,
        'allowed_filters': ['*'],
        'item_title': 'onion_exit',
        'resource_title': 'onions_exits',
        'projection': True,
        'sorting': True,
        'embedding': True,
        'embedded_fields': [''],
        'soft_delete': True,
        'pagination': True,
        'schema': {

            'hiddenService': {
                'type': 'string',

            },
            'port': {
                'type': 'string',

            },
            'address': {
                'type': 'string',

            },
            'fingerprint': {
                'type': 'string',
            },
            'nickname': {
                'type': 'string',

            },
            'locale': {
                'type': 'string',

            },

        }
    }

    return onions_exits
