import datetime
import json
import time
from helpers.chronuti import TimeStamp
from pprint import pprint

from flask import render_template
from app.models import Installation


def handleGithubAppPost(db, request, payload_queue):
    print("in handleGithubAppPost ...")
    message_id = request.headers.get('X-GitHub-Delivery')
    payload = json.loads(request.data)
    if "pull_request" in payload:
        envelope = {'message-id': message_id,
                    'timestamp' : TimeStamp.now().asISOString(),
                    'payload'   : payload}
        pprint(envelope)
        payload_queue.put_nowait(json.dumps(envelope).encode())
    print("received a payload via a POST from Github")
    return "received a payload via a POST from Github"


