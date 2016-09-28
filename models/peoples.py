# coding: utf8

"""
12/17/15 10:35 PM
model definition for peoples  document

"""
from security.bearer_auth import BoAuth

__author__ = 'clement'


def peoples():
    """
     by default, the standard item entry point is defined as
    '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    additional read-only entry point. This way consumers can also perform
    GET requests at '/people/<lastname>'.
    :return:  schema

    """
    to_bool = lambda v: v if type(v) is bool else str(v).lower() in ['true', '1', 'false', '0']
    peoples = {

        'additional_lookup': {
            'url': 'regex("[\w]+")',
            'field': 'owner'
        },
        'public_methods': ['GET'],
        'public_item_methods': ['GET', 'POST', 'DELETE'],
        'allowed_roles': ['admin', 'user'],
        'allowed_item_roles': ['admin', 'user'],
        'allowed_read_roles': ['user'],
        'allowed_write_roles': ['admin', 'user'],
        'allowed_item_read_roles': ['user'],
        'allowed_item_write_roles': ['admin', 'user'],
        'authentication': BoAuth,
        'allowed_filters': ['*'],
        'item_title': 'people',
        'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
        'resource_methods': ['POST', 'GET', 'DELETE'],
        'resource_title': 'peoples',
        'projection': True,
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

            'contact': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'contact_category': {'type': 'string'},
                        'contact_email': {'type': 'string'},
                        'contact_phone_mobile': {'type': 'string'},
                        'contact_phone_fix': {'type': 'string'},
                    },
                }
            },

            'socialised': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'socialised_category': {'type': 'string'},
                        'socialised_link': {'type': 'string'}
                    }
                }
            },
            'owner': {
                'type': 'objectid',
                'required': True,
                # referential integrity constraint: value must exist in the
                # 'people' collection. Since we aren't declaring a 'field' key,
                # will default to `people._id` (or, more precisely, to whatever
                # ID_FIELD value is).
                'data_relation': {
                    'resource': 'users',
                    # make the owner embeddable with ?embedded={"owner":1}
                    'embeddable': True,
                    'field': '_id'
                },
            },
            # 'role' is a list, and can only contain values from 'allowed'.
            'role': {
                'type': 'list',
                'allowed': ["admin", "freelancer", "recruiter", "user"],
            },
            # An embedded 'strongly-typed' dictionary.
            'location': {
                'type': 'dict',
                'schema': {
                    'address': {'type': 'string'},
                    'city': {'type': 'string'},
                    'postal_code': {'type': 'string'},
                    'geoloc': {
                        'type': 'point',

                    },

                },
            },

            'education': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'cursus_title': {'type': 'string'},
                        'cursus_location': {
                            'type': 'dict',
                            'schema': {
                                'school_name': {'type': 'string'},
                                'school_address': {'type': 'string'},
                                'school_postal_code': {'type': 'string'},
                                'school_link': {'type': 'string'},
                                'school_city': {'type': 'string'},
                                'school_geoloc': {'type': 'point'}
                            }
                        },
                        'cursus_date_start': {'type': 'datetime'},
                        'cursus_date_end': {'type': 'datetime'},
                        'cursus_status': {'type': 'string'},
                    }
                }
            },

            'born': {
                'type': 'datetime',

            },

            'about': {
                'type': 'string',
                'minlength': 5,
                'maxlength': 2500,

            },

            'works': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'company_name': {'type': 'string'},
                        'title': {'type': 'string'},
                        'area': {'type': 'string'},
                        'start': {'type': 'datetime'},
                        'end': {'type': 'datetime'},
                        'actual': {'type': 'boolean',
                                   'coerce': to_bool,
                                   'default': False},
                        'description': {'type': 'string'},

                    }
                }
            },
            'skills': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'skill_title': {
                            'type': 'string',
                            'required': True,
                        },
                        'skill_level': {
                            'type': 'string',
                            'required': True,
                        },
                        'skill_image': {
                            'type': 'string',
                        },
                        'skill_tag': {
                            'type': 'string',
                        }
                    }
                }
            }

        }

    }

    return peoples
