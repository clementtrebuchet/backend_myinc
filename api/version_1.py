# coding: utf8
"""

@Todo define use case

"""
import json

from eve import Eve
from flask import request
from flask.ext.cors import cross_origin
from flask.ext.sentinel import ResourceOwnerPasswordCredentials, oauth
import time
from eve_swagger import swagger

from security.bearer_auth import BoAuth


__author__ = 'clement'

app = Eve(auth=BoAuth)
ResourceOwnerPasswordCredentials(app)
app.register_blueprint(swagger)



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


def pre_get_promotion(resource, request, payload):
    """

    :param resource:
    :param request:
    :param payload:
    :return:
    """
    print('General pre_get_promotion {}\nRequest Headers: {}'
          '\nPayload: {}'.format(resource, request.headers, str(payload)))
    pass


def pre_post_peoples(resource, LocalProxy):
    """

    :param resource:
    :param request:
    :param payload:
    :return:
    """
    print('General pre_post_peoples')
    print(resource)
    print(LocalProxy.data)


def pre_patch_peoples(resource, request, opt):
    print('General pre_patch_peoples')
    print(resource)
    print(dir(request))
    print(request.get_json())
    print(opt)

@app.after_request
def after(response):
    """

    :param response:
    :return: add headers to http response
    """
    try:
        if request.headers['Origin']:
            response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            response.headers['Access-Control-Allow-Methods'] = "GET,POST,PUT,PATCH,DELETE,OPTIONS",
    except KeyError as error:
        print('{}'.format(error))
    return response


@app.route('/ping')
@cross_origin(origin='*')
# @oauth.require_oauth()
def heart_beat():
    """

    :return: call to know if api is online (only for users authenticated)
    """
    return json.dumps({
        'ts': '{}'.format(time.time()),
        'alive': 'pong'
    })


if __name__ == '__main__':
    app.on_fetched_resource += before_returning_peoples
    app.on_post_GET += post_get_callback
    app.on_pre_GET += pre_get_promotion
    app.on_pre_POST += pre_post_peoples
    app.on_pre_PATCH += pre_patch_peoples
    app.run(debug=True, host='192.168.0.2')
