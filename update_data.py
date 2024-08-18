import requests
import time
import json

# Enregistrer le temps de début global
start_time_global = time.time()

# Endpoint URL
url = 'https://api.sunflower-land.com/community/getFarms'
headers = {"Content-Type": "application/json"}

# Liste des proxies
proxy_list = [
    "http://52.124.19.86:3128",
    "http://141.164.86.18:3128",
    "http://172.252.163.146:3128",
    "http://69.58.68.104:3128",
    "http://69.58.70.12:3128",
]

# Lecture des IDs de ferme actifs depuis le fichier JSON
with open('actives.json', 'r') as json_file:
    active_farm_ids = json.load(json_file)

# Division des IDs de ferme actifs en lots de 100
batch_size = 100
active_farm_id_batches = [active_farm_ids[i:i+batch_size] for i in range(0, len(active_farm_ids), batch_size)]

# Créer une structure de données pour stocker les informations des fermes
all_farm_data = {}

# Itération à travers les lots et les proxies
for batch_num, batch in enumerate(active_farm_id_batches):
    proxy = proxy_list[batch_num % len(proxy_list)]  # Utilisation d'un proxy différent pour chaque lot

    print(f"Processing batch {batch_num + 1}/{len(active_farm_id_batches)} of {len(batch)} farms using proxy {proxy}")

    # Enregistrer le temps de début de la requête
    start_time_request = time.time()

    # Envoyer une requête en utilisant le proxy sélectionné
    data = {"ids": batch}
    response = requests.post(url, json=data, headers=headers, proxies={"http": proxy, "https": proxy})

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
                balance = farm_data.get('balance', {})
                bumpkin_data = farm_data.get('bumpkin', {})
                experience = bumpkin_data.get('experience', {})

                if farm_number not in all_farm_data:
                    all_farm_data[farm_number] = {}

                for item, quantity in inventory.items():
                    quantity_float = float(quantity)  # Convertir la quantité en nombre à virgule flottante
                    if item not in all_farm_data[farm_number]:
                        all_farm_data[farm_number][item] = 0
                    all_farm_data[farm_number][item] += quantity_float
				
                # Ajouter la balance associée à chaque ferme
                all_farm_data[farm_number]['Sfl'] = balance

                # Ajouter l'expérience associée à chaque ferme sous la clé "bumpkin"
                all_farm_data[farm_number]['Bumpkin'] = experience
    # Attendre 3 secondes avant de passer au prochain proxy
    time.sleep(3)

# Enregistrer les données dans un fichier JSON
with open('all_farm_data.json', 'w') as json_output:
    json.dump(all_farm_data, json_output, indent=4)

# Enregistrer le temps de fin global et calculer le temps d'exécution total
end_time_global = time.time()
execution_time_global = end_time_global - start_time_global

print("Data successfully updated in JSON file.")
print(f"Total execution time: {execution_time_global:.2f} seconds.")
