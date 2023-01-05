from flask import Flask, jsonify 
import collector 
import random
import time
from datetime import datetime


client_api = Flask(__name__)
system_id = f'system_{random.randint(100,999)}_{int(time.time())}' #creating a random unique system ID

@client_api.route('/get_util')
def get_util():
    start_time = time.time()
    payload = collector.get_collection()
    latency = round(time.time() - start_time, 3)
    collection_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    payload = {
        'id': system_id,
        'latency (sec)': latency,
        'collection_time': collection_time,
        'payload': payload
    }
    return jsonify(payload)


if __name__ == '__main__':
    client_api.run(ssl_context='adhoc')

