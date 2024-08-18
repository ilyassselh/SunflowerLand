from flask import Flask, jsonify
import json
import os
import threading
import time

app = Flask(__name__)
data_lock = threading.Lock()

# Keep track of last modification times
last_modified = {}

# Charger les données à partir des fichiers JSON
def load_fluctuations(period):
    with open(f'fluctuations_{period}.json') as json_file:
        return json.load(json_file)

# Thread function to periodically check and reload data
def check_and_reload_data():
    while True:
        with data_lock:
            for period in ['24h', '1h', '7d']:
                file_path = f'fluctuations_{period}.json'
                modified_time = os.path.getmtime(file_path)
                if period not in last_modified or last_modified[period] < modified_time:
                    last_modified[period] = modified_time
                    print(f"Reloading data for {period}")
            time.sleep(5)  # Wait for 5 seconds

# Start the data reloading thread
reload_thread = threading.Thread(target=check_and_reload_data)
reload_thread.daemon = True
reload_thread.start()

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
    app.run(host='0.0.0.0', port=1799)
