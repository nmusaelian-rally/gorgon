import time
import queue

from helpers.kafka import kafka


class PayloadPopulator:

    STOP_TOKEN = "HALT - No more work 4U"
    def __init__(self, topic_name, items):
        self.items = items # this is a queue.Queue instance
        self.kafka_producer = kafka()

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

