import requests
import time
import json
import os

# Enregistrer le temps de début global
start_time_global = time.time()

# Endpoint URL
url = 'https://api.sunflower-land.com/community/getFarms'
headers = {"Content-Type": "application/json"}

# Lecture des IDs de ferme actifs depuis le fichier JSON
with open('farm_top.json', 'r') as json_file:
    active_farm_ids = json.load(json_file)

# Division des IDs de ferme actifs en lots de 100
batch_size = 100
active_farm_id_batches = [active_farm_ids[i:i+batch_size] for i in range(0, len(active_farm_ids), batch_size)]

# Enregistrer les données dans un fichier JSON
output_filename = 'all_farm_data.json'
if not os.path.exists(output_filename):
    with open(output_filename, 'w') as json_output:
        json.dump({}, json_output)  # Initialize with an empty dictionary

with open(output_filename, 'r') as existing_json_file:
    try:
        all_farm_data = json.load(existing_json_file)
    except json.JSONDecodeError:
        all_farm_data = {}

# Itération à travers les lots
for batch_num, batch in enumerate(active_farm_id_batches):
    print(f"Processing batch {batch_num + 1}/{len(active_farm_id_batches)} of {len(batch)} farms")

    # Enregistrer le temps de début de la requête
    start_time_request = time.time()

    # Envoyer une requête
    data = {"ids": batch}
    response = requests.post(url, json=data, headers=headers)

    # Enregistrer le temps de fin de la requête et calculer le temps d'exécution
    end_time_request = time.time()
    execution_time_request = end_time_request - start_time_request
    print(f"Request execution time: {execution_time_request:.2f} seconds.")

    if response.status_code == 200:
        response_data = response.json()
        farms = response_data.get('farms', {})
        for farm_id, farm_data in farms.items():
            if farm_data != "None":
                farm_number = int(farm_id)
                inventory = farm_data.get('inventory', {})

                if farm_number not in all_farm_data:
                    all_farm_data[farm_number] = {}

                for item, quantity in inventory.items():
                    quantity_float = float(quantity)  # Convertir la quantité en nombre à virgule flottante
                    if item not in all_farm_data[farm_number]:
                        all_farm_data[farm_number][item] = 0
                    all_farm_data[farm_number][item] += quantity_float

    # Attendre 3 secondes avant de passer au prochain lot
    time.sleep(15)

# Enregistrer les données dans le fichier JSON existant
with open(output_filename, 'w') as json_output:
    json.dump(all_farm_data, json_output, indent=4)

# Enregistrer le temps de fin global et calculer le temps d'exécution total
end_time_global = time.time()
execution_time_global = end_time_global - start_time_global

print("Data successfully updated in JSON file.")
print(f"Total execution time: {execution_time_global:.2f} seconds.")
