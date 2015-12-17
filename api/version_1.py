# coding: utf8
"""

@Todo define use case

"""
from datetime import time
import json

from eve import Eve
from flask import request
from flask.ext.cors import cross_origin
from flask.ext.sentinel import ResourceOwnerPasswordCredentials, oauth

from security.bearer_auth import BoAuth

__author__ = 'clement'

app = Eve(auth=BoAuth)
ResourceOwnerPasswordCredentials(app)
app.config.from_object('settings')


def before_returning_peoples(resource_name, response):
    """

    :param resource_name:
    :param response:
    :return:do something with response before returning peoples
    """
    print('About to return items from {} '.format(resource_name))
    return response


def post_get_callback(resource, request, payload):
    """

    :param resource:
    :param request:
    :param payload:
    :return:
    """
    print('General GET callback asking resource {}\nRequest Headers: {}'
          '\nPayload: {}'.format(resource, request.headers, str(payload)))
    pass


@app.after_request
def after(response):
    """

    :param response:
    :return: add headers to http response
    """
    if request.headers['Origin']:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        response.headers['Access-Control-Allow-Headers'] = 'Authorization'
    return response


@app.route('/ping')
@cross_origin(origin='*')
@oauth.require_oauth()
def heart_beat():
    """

    :return: call to know if api is online (only for users authenticated)
    """
    return json.dumps({
        'ts': time(),
        'alive': 'pong'
    })


if __name__ == '__main__':
    app.on_fetched_resource += before_returning_peoples
    app.on_post_GET += post_get_callback
    app.run(debug=True)
