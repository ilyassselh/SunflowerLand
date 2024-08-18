import time
import requests
import asyncio
import schedule
import json

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

update = False  # Variable pour indiquer si une mise à jour est en cours

def get_resource_id(resource_name):
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
    
    if response.status_code == 200:
        data = response.json()
        nifty_price = data
        return nifty_price
    else:
        print("Request failed with status code:", response.status_code)
        return None
    
def format_price(price, qt):
    parsed_value = float(price)
    factor = 10**18
    reduction = 0.0294
    result = (parsed_value / factor) * (1 - reduction)
    return result * qt

# Fonction pour mettre à jour les prix précédents
def update_previous_prices(previous_prices):
    global update  # Utilisez la variable globale `update`
    update = True  # Définissez update sur True
    previous_prices.clear()
    print("Previous prices updated.")
    update = False  # Définissez update sur False lorsque la mise à jour est terminée

def calculate_fluctuations(interval, previous_prices, filename):
    while True:
        if update:  # Attendez si une mise à jour est en cours
            time.sleep(60)
            continue  # Passez à l'itération suivante

        new_fluctuations = {}

        for resource_name, resource_id in resource_ids.items():
            resource_price_data = get_nifty_price(resource_name)
            
            if resource_price_data is not None:
                price_dict = resource_price_data.get('prices', {})
                
                if resource_id in price_dict:
                    price_value = price_dict[resource_id]
                    current_price = format_price(price_value, 1)

                    if resource_name in previous_prices:
                        previous_price = previous_prices[resource_name]
                        price_variation = ((current_price - previous_price) / previous_price) * 100
                        new_fluctuations[resource_name] = {
                            "current_price": current_price,
                            "last_price": previous_price,
                            "percentage_change": price_variation
                        }
                    else:
                        previous_prices[resource_name] = current_price
                        new_fluctuations[resource_name] = {
                            "current_price": current_price,
                            "last_price": current_price,
                            "percentage_change": 0.0
                        }

        with open(filename, 'w') as json_file:
            json.dump(new_fluctuations, json_file, indent=2)
            
        print(f"\nFLUCTUATIONS UPDATED ({interval})\n//////")
        for resource_name, info in new_fluctuations.items():
            print(f"Resource: {resource_name.capitalize()}, Percentage Change in {interval}: {info['percentage_change']}%")
            
        time.sleep(interval)

async def main():
    previous_prices_24h = {}
    previous_prices_1h = {}
    previous_prices_7d = {}

    schedule.every().day.at("00:00").do(update_previous_prices, previous_prices_24h)
    schedule.every().hour.at(":00").do(update_previous_prices, previous_prices_1h)
    schedule.every().sunday.at("00:00").do(update_previous_prices, previous_prices_7d)

    # Start all tasks concurrently
    await asyncio.gather(
        calculate_fluctuations(500, previous_prices_24h, 'fluctuations_24h.json'),
        calculate_fluctuations(120, previous_prices_1h, 'fluctuations_1h.json'),
        calculate_fluctuations(1800, previous_prices_7d, 'fluctuations_7d.json'),
        reset_prices(),
    )

if __name__ == "__main__":
    asyncio.run(main())