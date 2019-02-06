import sys, os

from helpers.kafka import getConsumer, getProducer
from helpers       import dbconn
from helpers.prpar import parseAndDump
from threading     import Thread
from flask         import Flask

KAFKA_PAYLOAD_TOPIC  = 'ghooks'
KAFKA_RALLY_ITEMS    = 'rally_actions'
KAFKA_CONSUMER_GROUP = 'executive-banana-consumer-group'
ZOOKEEPER     = 'localhost:2181'
KAFKA_BROKERS = "localhost:9092,localhost:9003"

app = Flask(__name__)


@app.before_request
def before_request():
    consumer = getConsumer(KAFKA_PAYLOAD_TOPIC, KAFKA_CONSUMER_GROUP, ZOOKEEPER, KAFKA_BROKERS)
    producer = getProducer( ZOOKEEPER, KAFKA_BROKERS. KAFKA_RALLY_ITEMS)
    db       = dbconn.getConnection(os.environ['DATABASE_URL'])
    pt = Thread(target=parseAndDump, args=(consumer, producer, db))
    pt.daemon = True
    pt.start()

@app.route('/keepalive')
def entry_point():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)


