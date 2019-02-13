import time
import queue

from helpers.kafka import getProducer


KAFKA_PAYLOAD_TOPIC  = 'ghooks'
ZOOKEEPER     = 'localhost:2181'
KAFKA_BROKERS = "localhost:9092,localhost:9003"

class PayloadPopulator:

    STOP_TOKEN = "HALT - No more work 4U"
    def __init__(self, topic_name, items):
        self.items = items # this is a queue.Queue instance
        self.kafka_producer = getProducer(KAFKA_PAYLOAD_TOPIC, ZOOKEEPER, KAFKA_BROKERS)

    def work(self):

        while True:
            if not self.items.qsize():
                time.sleep(1)
                continue
            try:
                item = self.items.get(timeout=5.0)
            except queue.Empty:
                continue
            if item == PayloadPopulator.STOP_TOKEN:
                self.items.task_done()
                return True

            if item:
                self.kafka_producer.produce(item)
                self.items.task_done()

