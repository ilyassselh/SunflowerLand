import httpx
import discord
import asyncio
from datetime import datetime
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


async def get_nifty_price(resource_name):
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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                nifty_price = data
                return nifty_price
            else:
                print("Request failed with status code:", response.status_code)
                return None
        except Exception as e:
            print("Error:", str(e))
            return None

def send_webhook_alert(webhook_url, embed_data):
    if webhook_url is None:
        return

    response = requests.post(webhook_url, json={"embeds": [embed_data]})
    if response.status_code != 204:  # 204 No Content response indicates success
        print("Failed to send webhook alert!")

webhook_urls = [
    'https://discord.com/api/webhooks/1142913536390090762/MO1hkMnr1YO8rOjeZ56oCYpkyZ34M9-6qFLgcbC6-FWgVQwZT-XCQQIrkF6nGBtuaQzC',
    'https://discord.com/api/webhooks/1136412846587129958/K4D0RfxoMGvYo-IvItExT12WzwRh1ChFc4lkn91XG8Jhc6PWN6wEFIzliRnB6Xshgn_t'
]

role_ids = [1139359360242417765, 1113456056237047899]

top_prices = {}
bottom_prices = {}

async def nifty_snipe():
    previous_prices = {
    }
     
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
            resource_price_data = await get_nifty_price(resource_name)

            if resource_price_data is not None:
                price_dict = resource_price_data['prices']

                if resource_id in price_dict:
                    price_value = price_dict[resource_id]
                    formatted_price = format_price(price_value, 1)
                    
                    print(f"|{resource_name.capitalize()}: {formatted_price:.4f}|")
                    
                    # Mise à jour du dictionnaire des prix les plus élevés
                    if resource_name not in top_prices or formatted_price > top_prices[resource_name]:
                        top_prices[resource_name] = formatted_price

                    # Mise à jour du dictionnaire des prix les plus bas
                    if resource_name not in bottom_prices or formatted_price < bottom_prices[resource_name]:
                        bottom_prices[resource_name] = formatted_price
                    
                    if resource_name not in previous_prices:
                        previous_prices[resource_name] = None  # Initialize with None for the first iteration

                    previous_price = previous_prices[resource_name]

                    if previous_price is not None:
                        price_variation = ((formatted_price - previous_price) / previous_price) * 100
                        
                        min_variation_percentage = 10  # Minimum percentage change for triggering an alert

                        if abs(price_variation) >= min_variation_percentage:
                            change_type = "🟢" if price_variation > 0 else "🔴"
                            
                            
                            resource_image_url = f"https://sunflower-land.com/play/erc1155/images/{resource_id}.png"
                            resource_link = f"https://beta.niftyswap.io/collectible/polygon/0x22d5f9b75c524fec1d6619787e582644cd4d7422/{resource_id}?exchange=0x4e229569f61b8917d2b62a84715fffc614312084"
                            
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            for i, webhook_url in enumerate(webhook_urls):
                                role_id = role_ids[i]

                                embed_data = {
                                    "title": f"🚨 Price Alert for {resource_name.capitalize()}",
                                    "url": resource_link,
                                    "color": discord.Color.red().value if "🔴" in change_type else discord.Color.green().value,
                                    "thumbnail": {"url": resource_image_url},
                                    "description": f"<@&{role_id}>",
                                    "fields": [
                                        {"name": "💰 Last Price", "value": f"`{previous_price:.4f} SFL`", "inline": True},
                                        {"name": "🏷️ Price", "value": f"`{formatted_price:.4f} SFL`", "inline": True},
                                        {"name": "〽️ Percentage Change", "value": f"`{abs(price_variation):.2f}%`{change_type}", "inline": True}
                                    ],
                                    "footer": {"text": f"👑 Alert by ilyas_rifi 👑 | Alert Time: {current_time}"}
                                }

                                send_webhook_alert(webhook_url, embed_data, role_id)

                previous_prices[resource_name] = formatted_price

        print("________\nANALYSE des prix TERMINER\n________")
        await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(nifty_snipe())