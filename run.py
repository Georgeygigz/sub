from flask import Flask, render_template
import redis
import threading
import os
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)

r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0)

def my_callback(message):
    outp = f'Received message: {message["data"].decode()}'
    logger.info(outp)

def run_subscriber():
    logger.info("LISTENING >>>>>>>>>>>>>>>>>>")
    pubsub = r.pubsub()
    pubsub.subscribe('facility')
    for message in pubsub.listen():
        if message['type'] == 'message':
            my_callback(message)

@app.route('/')
def index():
    return {'msg': 'hello sub'}

@app.route('/subscribe')
def subscribe():
    threading.Thread(target=run_subscriber).start()
    return {'msg': 'sub started'}

if __name__ == '__main__':
    threading.Thread(target=run_subscriber).start()
    app.run(port=8080, host='0.0.0.0')
