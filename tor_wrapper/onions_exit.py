# coding: utf8
"""
This is the exits utility module


"""
url = 'https://curriculum.trebuchetclement.fr:5055/onions_exits'
__author__ = 'clement.trebuchet@gmail.com'


def exist_exit(hidden_service, http_client):
    """Check if this hidden_service exist in DataStore

    :param hidden_service: the hidden service name
    :type: str

    :param http_client: the http client
    :type: requests

    """
    response = http_client.get(r'{}/{}'.format(url, hidden_service))
    try:
        if response.status_code != 200:
            print(response.status_code, response.text)
            return False, response
        return True, response
    except Exception as e:
        print(e)
        return True, response


def patch_exit(client, gresponse, ressource):
    """Patch an existing entry in DataStore

    :param client: http client
    :type requests

    :param gresponse: http response
    :type requests.response

    :param ressource: the ressource from the rest api
    :type dict

    :return requests.response

    """
    etag = gresponse.json()['_etag']
    _id = gresponse.json()['_id']
    headers = {'If-Match': etag}
    presponse = client.patch(url='{}/{}'.format(url, _id), json=ressource, headers=headers)
    return presponse


def is_onions(expression):
    """Check if the given expression match an onion address

    :param:
        expression: expression to compare to

    :type:
        str

    :return: boolean

    """
    try:
        if expression.split('.')[1] == 'onion':
            return True
    except Exception as e:
        print(e)
        return False
    return False


def onion_model(controller, event, exit_relay):
    """Get a onions exit model, handle DataStore data representation

    :param controller: Stem Proxy Controller
    :type: stem.Controller

    :param event: Stem EventType
    :type: stem.response.events.Event

    :param exit_relay: Stem Relay
    :type: class:`~stem.descriptor.router_status_entry.RouterStatusEntry`

    :return: dict

    """
    data = {'hiddenService': "%s" % event.target.split(':')[0], 'port': "%s" % exit_relay.or_port,
            'address': "%s" % exit_relay.address, 'fingerprint': "%s" % exit_relay.fingerprint,
            'nickname': "%s" % exit_relay.nickname,
            'locale': "%s" % controller.get_info("ip-to-country/%s" % exit_relay.address, 'unknown')}
    return data


def say_it(controller, event, exit_relay, scan_result, err=False):
    """

    :param err:
    :type: boolean

    :param controller: Stem Proxy Controller
    :type: stem.Controller

    :param event: Stem EventType
    :type: stem.response.events.Event

    :param exit_relay: Stem Relay
    :type: class:`~stem.descriptor.router_status_entry.RouterStatusEntry`

    :param scan_result:
    :type: dict


    """
    if err:
        print('CREATE OK')
    else:
        print('CREATE OK %s' % scan_result['hiddenService'])

    print("Exit relay for our connection to %s" % (event.target.split(':')[0]))
    print("  address: %s:%i" % (exit_relay.address, exit_relay.or_port))
    print("  fingerprint: %s" % exit_relay.fingerprint)
    print("  nickname: %s" % exit_relay.nickname)
    print(
        "  locale: %s" % controller.get_info("ip-to-country/%s" % exit_relay.address,
                                             'unknown'))
    print("")


if __name__ == '__main__':
    pass
