from flask import Flask, jsonify 
import collector 

client_api = Flask(__name__)

@client_api.route('/get_util')
def get_util():
    return jsonify(collector.get_collection())


if __name__ == '__main__':
    client_api.run()

