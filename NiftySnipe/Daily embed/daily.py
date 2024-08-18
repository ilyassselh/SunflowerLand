import discord
from discord.ext import commands, tasks
import requests
from datetime import datetime, timedelta
import json
import time

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    description="__Bot by ilyas_rifi__👑\nhttps://discord.gg/TBPBmuvT\n\n**Support me**\n||``0x5a3adc9b55fa907809e7347fe9bfdecff2fdf55d``||"
)

@bot.event
async def on_ready():
    print(f"The bot has logged in as {bot.user}")

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.playing,
        name="👑 made by ilyas_rifi 👑"))

    daily_embed.start()  # Start the daily_embed loop

    
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

resource_data = {
    'sunflower': ('201', '🌻'),
    'potato': ('202', '🥔'),
    'pumpkin': ('203', '🎃'),
    'carrot': ('204', '🥕'),
    'cabbage': ('205', '🥬'),
    'beetroot': ('206', '🍆'),
    'cauliflower': ('207', '🥦'),
    'parsnip': ('208', '🌱'),
    'radish': ('209', '🍅'),
    'wheat': ('210', '🌾'),
    'kale': ('211', '🥗'),
    'apple': ('212', '🍎'),
    'blueberry': ('213', '🫐'),
    'orange': ('214', '🍊'),
    'eggplant': ('215', '🍆'),
    'wood': ('601', '🌳'),
    'stone': ('602', '🪨'),
    'iron': ('603', '⛏️'),
    'gold': ('604', '💰'),
    'egg': ('605', '🥚')
}

def create_price_embed(prices_data, current_prices):
    embed = discord.Embed(title="Daily Resource Prices", color=discord.Color.green())  # Change the color here

    for resource_info in prices_data.get('resources', []):
        resource_name = resource_info['resource']
        bottom_price = resource_info['bottom']
        top_price = resource_info['top']
        current_price = current_prices.get(resource_name, 0.0)
        emoji = resource_data.get(resource_name, ('', ''))[1]
        
        embed.add_field(
            name=f"{emoji} {resource_name.capitalize()}",
            value=f"Top Price: `{top_price:.4f} SFL`\nCurrent Price: `{current_price:.4f} SFL`\nBottom Price: `{bottom_price:.4f} SFL`",
            inline=True  # Display fields vertically for a better layout
        )

    embed.set_footer(text="👑 made by ilyas_rifi 👑")  # Add a footer text

    return embed

def fetch_current_prices():
    current_prices = {}  # Dictionary to store current prices

    for resource_name in resource_data:
        resource_price_data = get_nifty_price(resource_name)

        if resource_price_data is not None:
            price_dict = resource_price_data['prices']

            if resource_data[resource_name][0] in price_dict:
                price_value = price_dict[resource_data[resource_name][0]]
                formatted_price = format_price(price_value, 1)
                current_prices[resource_name] = formatted_price

    return current_prices

@tasks.loop(hours=12)  # Run every 12 hours
async def daily_embed():
    channel_id = 1140062884953595945 # Replace with the actual channel ID
    channel = bot.get_channel(channel_id)

    if channel:
        with open('prices_data.json', 'r') as json_file:
            prices_data = json.load(json_file)
            current_prices = fetch_current_prices()  # Fetch current prices
            embed = create_price_embed(prices_data, current_prices)
            await channel.send(embed=embed)
            
            # Calculate the time of the next alert
            current_time = datetime.now()
            next_alert_time = current_time + timedelta(hours=12)
            
            # Create an embed for the next alert time
            next_alert_embed = discord.Embed(title="Next Alert Time", color=discord.Color.blue())
            next_alert_embed.add_field(name="Next Alert at:", value=next_alert_time.strftime("%Y-%m-%d %H:%M:%S"))
            
            await channel.send(embed=next_alert_embed)
            
bot.run('')