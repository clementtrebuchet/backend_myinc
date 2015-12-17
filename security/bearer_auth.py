# coding: utf8
# @Todo define use case
"""
12/17/15 10:47 PM


"""
from eve.auth import BasicAuth
from flask import request
from redis import StrictRedis

__author__ = 'clement'


class BoAuth(BasicAuth):
    """ Overrides Eve's built-in basic authorization scheme and uses Redis to
    validate bearer token
    """

    def __init__(self):
        super(BoAuth, self).__init__()
        self.redis = StrictRedis()

    def check_auth(self, token, allowed_roles, resource, method):
        """ Check if API request is authorized.

        Examines token in header and checks Redis cache to see if token is
        valid. If so, request is allowed.

        :param token: BoAuth 2.0 access token submitted.
        :param allowed_roles: Allowed user roles.
        :param resource: Resource being requested.
        :param method: HTTP method being executed (POST, GET, etc.)
        """
        return token and self.redis.get(token)

    def authorized(self, allowed_roles, resource, method):
        """ Validates the the current request is allowed to pass through.

        :param allowed_roles: allowed roles for the current request, can be a
                              string or a list of roles.
        :param resource: resource being requested.
        """
        try:
            token = request.headers.get('Authorization').split(' ')[1]
        except:
            token = None
        return self.check_auth(token, allowed_roles, resource, method)