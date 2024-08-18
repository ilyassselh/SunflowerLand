from flask import Flask, jsonify
import json

app = Flask(__name__)

with open('all_farm_data.json', 'r') as file:
    farm_data = json.load(file)

@app.route('/getlist/<item>')
def get_item_quantity(item):
    result = []

    for farm_num, items in farm_data.items():
        if item in items:
            result.append({"farm_id": farm_num, "item_count": items[item]})

    result = sorted(result, key=lambda x: x["item_count"], reverse=True)
    
    for position, farm_info in enumerate(result, start=1):
        farm_info["position"] = position
    
    response = jsonify(result)
    response.headers['Content-Type'] = 'application/json'
    response.data = json.dumps(result, indent=4)
    
    return response

@app.route('/getlist/<item>/farm_id')
def get_farm_position(item):
    result = []

    for farm_num, items in farm_data.items():
        if item in items:
            result.append({"farm_id": farm_num, "item_count": items[item]})

    result = sorted(result, key=lambda x: x["item_count"], reverse=True)

    for position, farm_info in enumerate(result, start=1):
        if farm_info["farm_id"] == farm_num:
            return jsonify({"farm_id": farm_num, "position": position})
    
    return jsonify({"message": f"Item '{item}' not found in any farms."}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1798)