import os, sys

from helpers.kafka import getConsumer, getProducer
from helpers       import dbconn
from helpers.prpar import parseAndDump
from helpers.apparse import AppSettings
from threading     import Thread
from flask         import Flask

KAFKA_PAYLOAD_TOPIC  = 'ghooks'
KAFKA_RALLY_ITEMS    = 'rally_actions'
KAFKA_CONSUMER_GROUP = 'executive-banana-consumer-group'
ZOOKEEPER            = 'localhost:2181'
KAFKA_BROKERS        = "localhost:9092,localhost:9003"

app = Flask(__name__)
[AppSettings.loadEnvironment(app_file) for app_file in sys.argv[1:]]

def before_request():
    consumer = getConsumer(KAFKA_PAYLOAD_TOPIC, KAFKA_CONSUMER_GROUP, ZOOKEEPER, KAFKA_BROKERS)
    producer = getProducer(KAFKA_RALLY_ITEMS, ZOOKEEPER, KAFKA_BROKERS)
    connection = dbconn.getConnection(os.environ['DATABASE_URL'])
    pt = Thread(target=parseAndDump, args=(consumer, producer, connection))
    pt.daemon = True
    pt.start()

@app.route('/keepalive')
def entry_point():
    return 'parse service mode alive...'

if __name__ == '__main__':
    before_request()
    app.run(port=os.environ['PORT'])


