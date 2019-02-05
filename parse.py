import sys, os


from helpers.payloadparse import PayloadParser
from app.app import app

KAFKA_PAYLOAD_TOPIC = 'ghooks'
KAFKA_RALLY_ITEMS   = 'rally_actions'


if __name__ == '__main__':
    payload_parser = PayloadParser(KAFKA_PAYLOAD_TOPIC)
    payload_parser.work()
