import requests
import json
import time

url = "http://83.150.217.29:1796/getlist/Crow%20Feather"
threshold = 800
filtered_farm_ids = []

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for farm in data:
        if farm.get("item_count", 0) > threshold:
            filtered_farm_ids.append(int(farm.get("farm_id")))

    with open("farm_top.json", "w") as json_file:
        json.dump(filtered_farm_ids, json_file, indent=4)
else:
    print("Failed to retrieve data.")

    # Wait for 10 seconds before making the next request
    time.sleep(10)

print("Script completed.")