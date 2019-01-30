from flask import render_template
from app.models import Installation
import datetime
import json
from pprint import pprint
from helpers.kafka import kafka


def handleGithubAppPost(db, request):
    print("in handleGithubAppPost ...")
    message_id = request.headers.get('X-GitHub-Delivery')
    post_data = request.data
    payload = json.loads(post_data)
    kafka_producer = kafka()
    if "pull_request" in payload:
        pprint(payload)
        kafka_producer.produce(post_data)
    print("received a payload via a POST from Github")
    return "received a payload via a POST from Github"


