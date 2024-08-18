import requests
import datetime
import discord
import asyncio
import schedule
from datetime import datetime

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
    
    if response.status_code == 200:
        data = response.json()
        nifty_price = data
        return nifty_price
    else:
        print("Request failed with status code:", response.status_code)
        return None


def send_webhook_alert(webhook_url, embed_data):
    if webhook_url is None:
        return

    response = requests.post(webhook_url, json={"embeds": [embed_data]})
    if response.status_code != 204:  # 204 No Content response indicates success
        print("Failed to send webhook alert!")

webhook_url_1 = ''
webhook_url_2 = ''

role_id_1 = 
role_id_2 = 

previous_prices = {
}

async def nifty_snipe():
    global previous_prices, resetting_prices
    last_alert_percentages = {}
    
    while True:
        if resetting_prices:
            print("Resetting prices, pausing nifty_snipe...")
            await asyncio.sleep(60)  # Pause for 1 minute during reset
            resetting_prices = False
            print("Resuming nifty_snipe...")
        
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

                    if resource_name in previous_prices:
                        previous_price = previous_prices[resource_name]
                        price_variation = ((formatted_price - previous_price) / previous_price) * 100

                        min_variation_percentage = 10  # Minimum percentage change for triggering an alert
                        alert_threshold = 5  # Minimum percentage change to re-trigger an alert

                        if abs(price_variation) >= min_variation_percentage:
                            if resource_name in last_alert_percentages:
                                last_alert_percentage = last_alert_percentages[resource_name]

                                if abs(price_variation - last_alert_percentage) < alert_threshold:
                                    print(f"Alert already sent for {resource_name} and change is within threshold, skipping...")
                                    continue

                            last_alert_percentages[resource_name] = price_variation

                            change_type = "🟢" if price_variation > 0 else "🔴"

                            resource_image_url = f"https://sunflower-land.com/play/erc1155/images/{resource_id}.png"
                            resource_link = f"https://beta.niftyswap.io/collectible/polygon/0x22d5f9b75c524fec1d6619787e582644cd4d7422/{resource_id}?exchange=0x4e229569f61b8917d2b62a84715fffc614312084"

                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            # Create the embed for the webhook 1
                            embed_data_1 = {
                                "title": f"🚨 Price Alert for {resource_name.capitalize()} in 1h",
                                "url": resource_link,
                                "color": discord.Color.red().value if any("🔴" in alert for alert in change_type) else discord.Color.green().value,
                                "thumbnail": {"url": resource_image_url},
                                "description": f"<@&{role_id_1}>",  # Mention the role within the embed
                                "fields": [
                                    {"name": "💰 Last Price", "value": f"`{previous_price:.4f} SFL`", "inline": True},
                                    {"name": "🏷️ Price", "value": f"`{formatted_price:.4f} SFL`", "inline": True},
                                    {"name": "〽️ Percentage Change", "value": f"`{abs(price_variation):.2f}%`{change_type}", "inline": True}
                                ],
                                "footer": {"text": f"👑 Alert by ilyas_rifi 👑 | Alert Time: {current_time}"}
                            }

                            send_webhook_alert(webhook_url_1, embed_data_1)  # Send the alert via the first webhook

                            # Create the embed for the webhook 2
                            embed_data_2 = {
                                "title": f"🚨 Price Alert for {resource_name.capitalize()} in 1h",
                                "url": resource_link,
                                "color": discord.Color.red().value if any("🔴" in alert for alert in change_type) else discord.Color.green().value,
                                "thumbnail": {"url": resource_image_url},
                                "description": f"<@&{role_id_2}>",  # Mention the role within the embed
                                "fields": [
                                    {"name": "💰 Last 1h Price", "value": f"`{previous_price:.4f} SFL`", "inline": True},
                                    {"name": "🏷️ Price", "value": f"`{formatted_price:.4f} SFL`", "inline": True},
                                    {"name": "〽️ Percentage Change", "value": f"`{abs(price_variation):.2f}%`{change_type}", "inline": True}
                                ],
                                "footer": {"text": f"👑 Alert by ilyas_rifi 👑 | Alert Time: {current_time}"}
                            }

                            send_webhook_alert(webhook_url_2, embed_data_2)  # Send the alert via webhook

                        print(f"{resource_name.capitalize()} - Previous Price: {previous_price} - Formatted Price: {formatted_price}")

                    else:
                        previous_prices[resource_name] = formatted_price

        print("________\nANALYSE des prix TERMINÉE\n________")
        await asyncio.sleep(15)



# Define a flag to control the reset operation
resetting_prices = False

# Modify the reset_previous_prices function to use the flag
def reset_previous_prices():
    global previous_prices, resetting_prices
    resetting_prices = True
    previous_prices = {}
    print("Resetting previous prices 1h...")

# Modify the main function to run the nifty_snipe task
async def main():
    global resetting_prices
    
    # Start the nifty_snipe task
    nifty_task = asyncio.create_task(nifty_snipe())
    
    # Schedule the reset_previous_prices function
    schedule.every().hour.at(":00").do(reset_previous_prices)
    
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# Lancer la boucle d'événements asyncio
if __name__ == "__main__":
    asyncio.run(main())