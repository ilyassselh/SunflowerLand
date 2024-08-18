import json
import requests
import schedule
import asyncio
import time

def format_price(price, qt):
    parsed_value = float(price)
    factor = 10**18
    reduction = 0.0294
    result = (parsed_value / factor) * (1 - reduction)
    return result * qt

def get_resource_id(resource_name):
    resource_ids = {
        'sunflower': '201',
        'potato': '202',
        'pumpkin': '203',
        'carrot': '204',
        'cabbage': '205',
        'beetroot': '206',
        'cauliflower': '207',
        'parsnip': '208',
        'radish': '209',
        'wheat': '210',
        'kale': '211',
        'apple': '212',
        'blueberry': '213',
        'orange': '214',
        'eggplant': '215',
        'wood': '601',
        'stone': '602',
        'iron': '603',
        'gold': '604',
        'egg': '605'
}

    if resource_name in resource_ids:
        return resource_ids[resource_name]
    else:
        return None

def get_nifty_price(resource_name):
    resource_id = get_resource_id(resource_name)
    if resource_id is None:
        return None

    url = 'https://metadata.sequence.app/rpc/Metadata/GetNiftyswapUnitPrices'

    payload = {
        'chainId': '137',
        'contractAddress': '0x4e229569f61b8917d2b62a84715fffc614312084',
        'req': {
            'swapType': 'BUY',
            'ids': [resource_id],
            'amounts': ['1000000000000000000']
        },
        'fresh': True
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, json=payload)
    
    retry = True
    if response.status_code == 200:
        data = response.json()
        nifty_price = data
        return nifty_price
    elif response.status_code == 502 and retry:
        print("Request failed with status code 502. Retrying in 2 seconds...")
        time.sleep(2)  # Wait for 2 seconds and retry
        return get_nifty_price(resource_name)  # Retry without recursion
    else:
        print("Request failed with status code:", response.status_code)
        return None

top_prices = {}
bottom_prices = {}

async def nifty_snipe():
    while True:
        resource_ids = {
            'sunflower': '201',
            'potato': '202',
            'pumpkin': '203',
            'carrot': '204',
            'cabbage': '205',
            'beetroot': '206',
            'cauliflower': '207',
            'parsnip': '208',
            'radish': '209',
            'wheat': '210',
            'kale': '211',
            'apple': '212',
            'blueberry': '213',
            'orange': '214',
            'eggplant': '215',
            'wood': '601',
            'stone': '602',
            'iron': '603',
            'gold': '604',
            'egg': '605'
        }

        for resource_name, resource_id in resource_ids.items():
            resource_price_data = get_nifty_price(resource_name)

            if resource_price_data is not None:
                price_dict = resource_price_data['prices']

                if resource_id in price_dict:
                    price_value = price_dict[resource_id]
                    formatted_price = format_price(price_value, 1)

                    if resource_name not in top_prices or formatted_price > top_prices[resource_name]:
                        top_prices[resource_name] = formatted_price

                    if resource_name not in bottom_prices or formatted_price < bottom_prices[resource_name]:
                        bottom_prices[resource_name] = formatted_price

                    print(f"{resource_name.capitalize()}: {formatted_price:.4f}")

        # Enregistrement des données dans un fichier JSON
        data_to_save = {'resources': []}
        for resource_name in resource_ids:
            data_to_save['resources'].append({
                'resource': resource_name,
                'bottom': bottom_prices.get(resource_name, 0),
                'top': top_prices.get(resource_name, 0)
            })

        with open('prices_data.json', 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)

        await asyncio.sleep(15)

def reset_prices():
    global top_prices, bottom_prices
    top_prices = {}
    bottom_prices = {}

# Ajoutez cette ligne à la fin de votre code pour planifier la réinitialisation quotidienne à 20h
schedule.every().day.at("20:00").do(reset_prices)        
        
if __name__ == "__main__":
    # Lancer la tâche asynchrone pour récupérer les prix
    asyncio.run(nifty_snipe())

    # Lancer la boucle de planification de schedule
    while True:
        schedule.run_pending()
        time.sleep(1)