import sys
import time
from helpers.kafka import  kafka


from flask import Flask

app = Flask(__name__)
@app.before_request
def before_request():
    consumer = kafka.getConsumer('ghooks', 'executive-banana-consumer-group')
    producer = kafka.getProducer('rally-actions')
    db       =


@app.route('/keepalive')
def entry_point():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
