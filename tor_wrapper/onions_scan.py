# coding: utf8
import functools
import json
import multiprocessing
import random
import signal
import subprocess
import sys
import time
from threading import Event
from threading import Timer

import codecs
import os
import requests
from stem import Signal, StreamStatus
from stem.control import Controller, EventType

from tor_wrapper.onions_exit import is_onions, onion_model, say_it, patch_exit, exist_exit

onions = []
session_onions = []
url = 'https://curriculum.trebuchetclement.fr:5055/onions'
PASSWD = "***************"


def run_exit_scan(http_client):
    """

    :param http_client:
    :type: requests.client
    :return:
    """
    print("Tracking requests for tor exits. Press 'enter' to end.")
    with Controller.from_port() as controller:
        try:
            DO = True
            controller.authenticate(PASSWD)
            stream_listener = functools.partial(stream_event, controller, http_client=http_client)
            controller.add_event_listener(stream_listener, EventType.STREAM)
            while DO:
                time.sleep(500)
                print('[exit] Alive')
        except KeyboardInterrupt:
            print('[!!]Keyboard interrupt')
        except Exception as e:
            print(e)
            print('[**]Exception {}'.format(e))


def stream_event(controller, event, http_client=None):
    """CallBack for event listener

    :param controller:
    :param event:
    """
    if event.status == StreamStatus.SUCCEEDED and event.circ_id:
        try:
            circ = controller.get_circuit(event.circ_id)
            exit_fingerprint = circ.path[-1][0]
            exit_relay = controller.get_network_status(exit_fingerprint)
            onni = is_onions(event.target.split(':')[0])
            if onni:
                print('[***] Exit relay {}'.format(event.target))
                model_exist, model_response = exist_exit(event.target.split(':')[0], http_client)
                if not model_exist:
                    scan_result = onion_model(controller, event, exit_relay)
                    response = http_client.post(url=url, json=scan_result)
                    if response.status_code != 201 and response.status_code != 401:
                        print(response, response.status_code, response.text)
                    elif response.status_code == 401:
                        http_client = get_client()
                        response = http_client.post(url=url, json=scan_result)
                        if response.status_code != 201 and response.status_code != 401:
                            print(response, response.status_code, response.text)
                        else:
                            try:
                                say_it(controller, event, exit_relay, scan_result)
                            except Exception as e:
                                print(e)
                                say_it(controller, event, exit_relay, scan_result, err=True)
                    else:
                        try:
                            say_it(controller, event, exit_relay, scan_result)
                        except Exception as e:
                            print(e)
                            say_it(controller, event, exit_relay, scan_result, err=True)
                elif model_exist and is_onions(event.target.split(':')[0]):
                    scan_result = onion_model(controller, event, exit_relay)
                    patch_exit(http_client, model_response, json.dumps(scan_result))
                else:
                    pass

        except Exception as e:
            print(e)


def add(ressource, http_client):
    """Add a result form onion_scan go routine

    :param http_client:
    :type requests.client

    :param ressource:
    :type dict


    """
    global onions
    global session_onions

    # look for additional .onion domains to add to our scan list
    scan_result = ur"%s" % ressource.decode("utf8")
    scan_result = json.loads(scan_result)

    if scan_result['linkedSites'] is not None:
        add_new_onions(scan_result['linkedSites'])

    if scan_result['relatedOnionDomains'] is not None:
        add_new_onions(scan_result['relatedOnionDomains'])

    if scan_result['relatedOnionServices'] is not None:
        add_new_onions(scan_result['relatedOnionServices'])
    if not scan_result['webDetected']:
        print("[**!!]Not a webSite")
        return
    elif not exist(scan_result['hiddenService'], http_client):
        response = http_client.post(url=url, json=scan_result)
        if response.status_code != 201 and response.status_code != 401:
            print(response, response.status_code, response.text)
        elif response.status_code == 401:
            http_client = get_client()
            response = http_client.post(url=url, json=scan_result)
            if response.status_code != 201 and response.status_code != 401:
                print(response, response.status_code, response.text)
            else:
                try:
                    print('CREATE OK %s' % scan_result['hiddenService'])
                except Exception:
                    print('CREATE OK')
        else:
            try:
                print('CREATE OK %s' % scan_result['hiddenService'])
            except Exception:
                print('CREATE OK')

    else:
        __patch(scan_result, http_client)

    return


def __patch(ressource, http_client):
    """

    :param ressource: dict
        a json dict
    :return:
    """

    gresponse = http_client.get(url='{}/{}'.format(url, ressource['hiddenService']))
    if gresponse.status_code != 200:
        print(gresponse, gresponse.status_code, gresponse.text)
    else:
        presponse = patch_it(http_client, gresponse, ressource)
        if presponse.status_code == 200:
            print('PATCHED OK {}'.format(ressource['hiddenService']))
        elif presponse.status_code == 401:
            http_client = get_client()
            presponse = patch_it(http_client, gresponse, ressource)
            if presponse.status_code == 200:
                print('PATCHED OK {}'.format(ressource['hiddenService']))
            else:
                print('PATCHED KO {} {}'.format(ressource['hiddenService'], presponse.text))

        else:
            print('PATCHED KO {} {}'.format(ressource['hiddenService'], presponse.text))


def patch_it(client, gresponse, ressource):
    """

    :param client:
    :param gresponse:
    :param ressource:
    :return:

    """
    etag = gresponse.json()['_etag']
    _id = gresponse.json()['_id']
    headers = {'If-Match': etag}
    presponse = client.patch(url='{}/{}'.format(url, _id), json=ressource, headers=headers)
    return presponse


def exist(hidden_service, http_client):
    """check if an onions is already in the DataStore

    :param hidden_service:
    ;type: str

    :return: boolean

    """
    try:
        response = http_client.get(ur'{}/{}'.format(url, hidden_service))
        if response.status_code != 200:
            print(response.status_code, response.text)
            return False
        return True
    except Exception as e:
        print(e)
        return True


#
# Grab the list of onions from our master list file.
#
def get_onion_list(url_list=None):
    """

    :param url_list:
    :type: list


    :return: list

    """
    if url_list is None:
        # open the master list
        if os.path.exists("onion_master_list.txt"):

            with open("onion_master_list.txt", "rb") as fd:

                stored_onions = fd.read().splitlines()
        else:
            print("[!] No onion master list. Download it!")
            sys.exit(0)

    else:
        stored_onions = []
        stored_onions.extend(url_list)

    print("[*] Total onions for scanning: %d" % len(stored_onions))
    return stored_onions


#
# Stores an onion in the master list of onions.
#
def store_onion(onion):
    """Store an onion in the master file onions process list

    :param onion:
    :type: str


    :return:

    """
    print("[++] Storing %s in master list." % onion)

    with codecs.open("onion_master_list.txt", "ab", encoding="utf8") as fd:
        fd.write("%s\n" % onion)

    return


#
# Runs onion scan as a child process.
#
def run_onionscan(onion, identity_lock):
    """Wrapper around  the go onionscan bin

    :param onion:
    :type: str

    :param identity_lock:
    :type: stem.Event


    """

    print("[*] Onionscanning %s" % onion)

    # fire up onionscan
    process = subprocess.Popen(["/home/clement/.gvm/pkgsets/go1.4/global/bin/onionscan",
                                "--jsonReport", "--simpleReport=false", onion], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # start the timer and let it run 5 minutes
    process_timer = Timer(300, handle_timeout, args=[process, onion, identity_lock])
    process_timer.start()

    try:
        # wait for the onion scan results
        stdout = process.communicate()[0]
    except KeyboardInterrupt:
        process_timer.cancel()
        process.kill()
        exit(0)

    # we have received valid results so we can kill the timer
    if process_timer.is_alive():
        process_timer.cancel()
        return stdout

    print("[!!!] Process timed out!")

    return None


#
# Handle a timeout from the onionscan process.
#
def handle_timeout(process, onion, identity_lock):
    """

    :param process:
    :param onion:
    :param identity_lock:

    :return:
    """
    # halt the run_exit_scan thread while we grab a new identity
    identity_lock.clear()

    # kill the onionscan process
    try:
        process.kill()
        print("[!!!] Killed the onionscan process.")
    except:
        pass

    # Now we switch TOR identities to make sure we have a good connection
    with Controller.from_port(port=9051) as torcontrol:

        # authenticate to our local TOR controller
        torcontrol.authenticate(PASSWD)

        # send the signal for a new identity
        torcontrol.signal(Signal.NEWNYM)

        # wait for the new identity to be initialized
        time.sleep(torcontrol.get_newnym_wait())

        print("[!!!] Switched TOR identities.")

    # push the onion back on to the list
    session_onions.append(onion)
    random.shuffle(session_onions)
    # allow the run_exit_scan thread to resume executing
    identity_lock.set()

    return


#
# Processes the JSON result from onionscan.
#
def process_results(onion, json_response):
    """

    :param onion:
    :param json_response:
    :return:

    """
    global onions
    global session_onions

    # create our output folder if necessary
    if not os.path.exists("onionscan_results"):
        os.mkdir("onionscan_results")

    # write out the JSON results of the scan
    with open("%s/%s.json" % ("onionscan_results", onion), "wb") as fd:
        fd.write(json_response)

    # look for additional .onion domains to add to our scan list
    scan_result = ur"%s" % json_response.decode("utf8")
    scan_result = json.loads(scan_result)

    if scan_result['linkedSites'] is not None:
        add_new_onions(scan_result['linkedSites'])

    if scan_result['relatedOnionDomains'] is not None:
        add_new_onions(scan_result['relatedOnionDomains'])

    if scan_result['relatedOnionServices'] is not None:
        add_new_onions(scan_result['relatedOnionServices'])

    return


#
# Handle new onions.
#
def add_new_onions(new_onion_list):
    """

    :param new_onion_list:

    :return:

    """
    global onions
    global session_onions

    for linked_onion in new_onion_list:

        if linked_onion not in onions and linked_onion.endswith(".onion"):
            print("[++] Discovered new .onion => %s" % linked_onion)

            onions.append(linked_onion)
            session_onions.append(linked_onion)
            random.shuffle(session_onions)
            store_onion(linked_onion)

    return


process_holder = []


def scan(mongo=True, url_list=None):
    """

    :param mongo:
    :param url_list:
    :return:

    """
    global process_holder
    identity_lock = Event()
    identity_lock.set()

    # get a list of onions to process
    onions = get_onion_list(url_list=url_list)

    # randomize the list a bit
    random.shuffle(onions)

    session_onions = list(onions)
    http_client = get_client()
    http_client_exit = get_client()
    count = 0
    while True:
        # if the event is cleared we will halt here
        # otherwise we continue executing
        identity_lock.wait()
        # grab a new onion to scan
        print("[*] Running %d of %d." % (count, len(onions)))
        process_holder.append(multiprocessing.Process(target=run_exit_scan, name='exit_scan', args=[http_client_exit]))
        for p in process_holder:
            p.start()
            p.join(timeout=1)

        print("[*] Detach Exit Tor Relay scan")

        try:
            onion = session_onions.pop()
        except IndexError as e:
            if url_list is not None:
                print('[!!!] this is a one shot url list {}'.format(url_list))
                signal.signal(signal.SIGALRM, handler)
                break
            try:
                print('Error cannot retrieve onions in list {}'.format(e))
                onions = get_onion_list(url_list=url_list)
                print('get onions - list length {}'.format(len(onions)))
                session_onions = list(onions)
                print('get session_onions - list length {}'.format(len(session_onions)))
                count = 0
                print('reset counter {}'.format(count))
                continue
            except Exception as e:
                print('[!!!] cannot reload onions list {}'.format(e))
                signal.signal(signal.SIGALRM, handler)
                break

        # test to see if we have already retrieved results for this onion
        if not mongo:
            if os.path.exists("onionscan_results/%s.json" % onion):
                print("[!] Already retrieved %s. Skipping." % onion)
                count += 1
                continue

        # run the onion scan
        result = run_onionscan(onion, identity_lock, )

        # process the results
        if result is not None and not mongo:
            if len(result):
                process_results(onion, result)
                count += 1
        elif result is not None and mongo:
            if len(result):
                add(result, http_client)
                count += 1


def handler(signum, frame):
    """

    :param signum:
    :param frame:
    :return:

    """
    try:
        for p in process_holder:
            p.terminate()
    except Exception:
        pass


def get_client():
    """

    :return:
    """

    http_session = requests.session()
    http_session.headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    resp = http_session.post(
        url='https://curriculum.trebuchetclement.fr:5055/oauth/token?client_id=YM5Qe9Ho6YfecEKQaMXZtbw9edPS6KhT0iKZ6FUf&grant_type=password&username={}&password={}'.format(
            'messagebot', 'messagebot'))
    access_token = resp.json()['access_token']
    print('Get access token', access_token)
    http_session.headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    return http_session


if __name__ == '__main__':
    scan()
