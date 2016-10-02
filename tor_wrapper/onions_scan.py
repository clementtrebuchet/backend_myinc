# coding: utf8
import json
import random
import subprocess
import sys
import time
from threading import Event
from threading import Timer

import codecs
import os
import requests
from stem import Signal
from stem.control import Controller

onions = []
session_onions = []
url = 'https://curriculum.trebuchetclement.fr:5055/onions'
PASSWD = "..."


def add(ressource, client):
    """

    :param ressource: dict
        a json dict

    :return:
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

    if not exist(scan_result['hiddenService'], client):
        response = client.post(url=url, json=scan_result)
        if response.status_code != 201:
            print(response, response.status_code, response.text)
        else:
            try:
                print('CREATE OK %s'% scan_result['hiddenService'])
            except Exception:
                print('CREATE OK')

    else:
        __patch(scan_result, client)

    return


def __patch(ressource, client):
    """

    :param ressource: dict
        a json dict
    :return:
    """
    gresponse = client.get(url='{}/{}'.format(url, ressource['hiddenService']))
    if gresponse.status_code != 200:
        print(gresponse, gresponse.status_code, gresponse.text)
    else:
        etag = gresponse.json()['_etag']
        _id = gresponse.json()['_id']
        headers = {'If-Match': etag}
        presponse = client.patch(url='{}/{}'.format(url, _id), json=ressource, headers=headers)
        if presponse.status_code == 200:
            print('PATCHED OK {}'.format(ressource['hiddenService']))
        else:
            print('PATCHED KO {} {}'.format(ressource['hiddenService'], presponse.text))


def exist(hidden_service, client):
    """

    :param hidden_service:
    :return:
    """
    try:
        response = client.get(ur'{}/{}'.format(url, hidden_service))
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
def get_onion_list():
    # open the master list
    if os.path.exists("onion_master_list.txt"):

        with open("onion_master_list.txt", "rb") as fd:

            stored_onions = fd.read().splitlines()
    else:
        print("[!] No onion master list. Download it!")
        sys.exit(0)

    print("[*] Total onions for scanning: %d" % len(stored_onions))

    return stored_onions


#
# Stores an onion in the master list of onions.
#
def store_onion(onion):
    print("[++] Storing %s in master list." % onion)

    with codecs.open("onion_master_list.txt", "ab", encoding="utf8") as fd:
        fd.write("%s\n" % onion)

    return


#
# Runs onion scan as a child process.
#
def run_onionscan(onion, identity_lock):
    """

    :param onion:
    :param identity_lock:
    :return:
    """
    print("[*] Onionscanning %s" % onion)

    # fire up onionscan
    process = subprocess.Popen(["/home/clement/.gvm/pkgsets/go1.4/global/bin/onionscan",
                                "--jsonReport", "--simpleReport=false", onion], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # start the timer and let it run 5 minutes
    process_timer = Timer(300, handle_timeout, args=[process, onion, identity_lock])
    process_timer.start()

    # wait for the onion scan results
    stdout = process.communicate()[0]

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
    # halt the main thread while we grab a new identity
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
    # allow the main thread to resume executing
    identity_lock.set()

    return


#
# Processes the JSON result from onionscan.
#
def process_results(onion, json_response):
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


def main(mongo=True):
    """

    :return:

    """
    identity_lock = Event()
    identity_lock.set()

    # get a list of onions to process
    onions = get_onion_list()

    # randomize the list a bit
    random.shuffle(onions)

    session_onions = list(onions)
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
    count = 0
    while count < len(onions):
        # if the event is cleared we will halt here
        # otherwise we continue executing
        identity_lock.wait()

        # grab a new onion to scan
        print ("[*] Running %d of %d." % (count, len(onions)))

        try:
            onion = session_onions.pop()
        except IndexError as e:
            print('Error cannot retrieve onions in list {}'.format(e))
            del onions
            onions = get_onion_list()
            del count
            count = 0
            continue

        # test to see if we have already retrieved results for this onion
        if not mongo:
            if os.path.exists("onionscan_results/%s.json" % onion):
                print("[!] Already retrieved %s. Skipping." % onion)
                count += 1
                continue

        # run the onion scan
        result = run_onionscan(onion, identity_lock)

        # process the results
        if result is not None and not mongo:
            if len(result):
                process_results(onion, result)
                count += 1
        elif result is not None and mongo:
            if len(result):
                add(result, http_session)
                count += 1


if __name__ == '__main__':
    main()
