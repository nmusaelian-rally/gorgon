import os, sys
import time
import json
import requests

from helpers.kafka import getConsumer
from helpers.apparse import AppSettings
from threading     import Thread
from flask         import Flask

KAFKA_RALLY_ITEMS    = 'rally_actions'
KAFKA_CONSUMER_GROUP = 'executive-papaya-consumer-group'
ZOOKEEPER     = 'localhost:2181'
KAFKA_BROKERS = "localhost:9092,localhost:9003"
RALLY_URL     = 'https://rally1.rallydev.com/slm/webservice/v2.0/pullrequest/create'


app = Flask(__name__)
[AppSettings.loadEnvironment(app_file) for app_file in sys.argv[1:]]

def postPRtoRally(consumer):
    for message in consumer: # iterate over consumer, pulling out payload items
        m = json.loads(message.value.decode())
        print("postPRtoRally pulled off a message from the rally_actions topic...")
        pull_request = m['rally_payload']

        if 'api_key' not in m:
            m['api_key'] = '_2QFAQA0wQoSKiORUOsVlMjeQfFr1JkawtItGFHtrtx8'
        headers  = {'zsessionid': m['api_key'],'content-type':'application/json'}
        params   = {'workspace' : m['workspace']}
        response = None
        print(pull_request)
        try:
            #response = requests.post(RALLY_URL, headers=headers, params=params, json=json.dumps(pull_request))
            response = requests.post(RALLY_URL, headers=headers, params=params, data=json.dumps(pull_request))
            print("response status: %s" % (response.status_code))
            print(response.text)
        except requests.exceptions.RequestException as ex:
            print(ex)

def before():
    consumer = getConsumer(KAFKA_RALLY_ITEMS,   KAFKA_CONSUMER_GROUP, ZOOKEEPER, KAFKA_BROKERS)
    pt = Thread(target=postPRtoRally, args=(consumer,))
    pt.daemon = True
    pt.start()
    return pt


@app.route('/keepalive')
def entry_point():
    return 'post service mode alive...'


if __name__ == '__main__':
    post_thread = before()
    app.run(port=os.environ['PORT'])
    post_thread.join()








