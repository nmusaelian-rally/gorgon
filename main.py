import sys, os
import threading
from queue import Queue

from helpers.payloadpop import PayloadPopulator
from app.app import app


MAX_QUEUE_SIZE = 100
KAFKA_PAYLOAD_TOPIC = 'ghooks'


if __name__ == '__main__':
    payload_queue = Queue(maxsize=MAX_QUEUE_SIZE)
    app.payload_queue = payload_queue
    payload_populator = PayloadPopulator(KAFKA_PAYLOAD_TOPIC, payload_queue)
    pt = threading.Thread(target=payload_populator.work)
    pt.daemon = True
    pt.start()

    print("about to run the app...")
    app.run(port=os.environ['PORT'])
    pt.join()