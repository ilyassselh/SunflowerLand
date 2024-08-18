from flask import Flask, jsonify
import json

app = Flask(__name__)

# Charger les données à partir des fichiers JSON
def load_fluctuations(period):
    with open(f'fluctuations_{period}.json') as json_file:
        return json.load(json_file)

@app.route('/fluctuations/24h', methods=['GET'])
def get_fluctuations_24h():
    fluctuations_24h = load_fluctuations('24h')
    return jsonify(fluctuations_24h)

@app.route('/fluctuations/1h', methods=['GET'])
def get_fluctuations_1h():
    fluctuations_1h = load_fluctuations('1h')
    return jsonify(fluctuations_1h)

@app.route('/fluctuations/7d', methods=['GET'])
def get_fluctuations_7d():
    fluctuations_7d = load_fluctuations('7d')
    return jsonify(fluctuations_7d)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1988)