# coding: utf8
"""
Tor web parser Parser

"""
__author__ = 'clement.trebuchet'
# coding: utf8
"""
12/17/15 10:33 PM
model definition for peoples skills document

"""
from security.bearer_auth import BoAuth



def onions():
    """

    :return:skills schema
    """
    onions = {
        'cache_control': 'max-age=10,must-revalidate',
        'cache_expires': 10,
        'additional_lookup': {
            'url': 'regex("\w+\.\w+")',
            'field': 'hiddenService'
        },
        'public_methods': ['GET', 'POST', 'DELETE', 'PATCH'],
        'public_item_methods': ['GET', 'POST', 'DELETE'],
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
        'item_title': 'onion',
        'resource_title': 'onions',
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
            'dateScanned': {
                'type': 'string',

            },
            'webDetected': {
                'type': 'boolean',
            },
            'tlsDetected': {
                'type': 'boolean',

            },
            'sshDetected': {
                'type': 'boolean',

            },
            'ricochetDetected': {
                'type': 'boolean',

            },
            'ircDetected': {
                'type': 'boolean',

            },
            'smtpDetected': {
                'type': 'boolean',

            },
            'ftpDetected': {
                'type': 'boolean',

            },
            'bitcoinDetected': {
                'type': 'boolean',

            },
            'mongodbDetected': {
                'type': 'boolean',

            },
            'vncDetected': {
                'type': 'boolean',

            },
            'xmppDetected': {
                'type': 'boolean',

            },
            'skynetDetected': {
                'type': 'boolean',

            },
            'privateKeyDetected': {
                'type': 'boolean',

            },
            'serverPoweredBy': {
                'type': 'string',

            },
            'serverVersion': {
                'type': 'string',

            },
            'foundApacheModStatus': {
                'type': 'boolean',

            },
            'relatedOnionServices': {
                'type': 'list',
                'nullable': True,

            },
            'relatedOnionDomains': {
                'type': 'list',
                'nullable': True,
            },
            'linkedSites': {
                'type': 'list',
                'nullable': True,

            },
            'internalPages': {
                'type': 'list',
                'nullable': True,

            },
            'ipAddresses': {
                'type': 'list',
                'nullable': True,

            },
            'openDirectories': {
                'type': 'list',
                'nullable': True,

            },
            'exifImages': {
                'type': 'list',
                'nullable': True,

            },
            'interestingFiles': {
                'type': 'list',
                'nullable': True,

            },
            'pageReferencedDirectories': {
                'type': 'list',
                'nullable': True,

            },
            'pgpKeys': {
                'type': 'list',
                'nullable': True,

            },
            'hashes': {
                'type': 'list',
                'nullable': True,

            },
            'snapshot': {
                'type': 'string',

            },
            'pageTitle': {
                'type': 'string',

            },
            'responseHeaders': {
                'type': 'dict',

            },
            'certificates': {
                'type': 'list',
                'nullable': True,

            },
            'bitcoinAddresses': {
                'type': 'list',
                'nullable': True,

            },
            'sshKey': {
                'type': 'string',

            },
            'sshBanner': {
                'type': 'string',

            },
            'ftpFingerprint': {
                'type': 'string',

            },
            'ftpBanner': {
                'type': 'string',

            },
            'smtpFingerprint': {
                'type': 'string',

            },
            'smtpBanner': {
                'type': 'string',

            },
            'lastAction': {
                'type': 'string',

            },
            'TimedOut': {
                'type': 'boolean',

            },
        }
    }
    return onions
