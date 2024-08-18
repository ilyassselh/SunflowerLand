import requests
import discord
from discord.ext import commands
import asyncio


intents = discord.Intents.all()
intents.messages = True
intents.guilds = True

bot = commands.AutoShardedBot(
    command_prefix="!",
    intents=intents,
    description="__Bot by ilyas_rifi__👑\nhttps://discord.gg/TBPBmuvT\n\n**Support me**\n||``0x5a3adc9b55fa907809e7347fe9bfdecff2fdf55d``||"
)

def get_goblin_price(sflitem_name):
    sfltools = requests.get('https://sfl.tools/api/listings/prices')
    sfltools_json = sfltools.json()  # Parse JSON response
    
    for item in sfltools_json.values():
        if item['sflItemName'].lower() == sflitem_name.lower():
            return item  # Return the entire item data
    
    return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(
                              type=discord.ActivityType.playing,
                              name="👑 made by ilyas_rifi 👑"))
    previous_prices = {
        'wood': 0.03,  # Previous price for wood
        'iron': 2.5,   # Previous price for iron
        'gold': 100    # Previous price for gold
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
            resource_price_data = get_goblin_price(resource_name)
            
            if resource_price_data is not None:
                price_dict = resource_price_data['pricePerUnitTaxed']
                
                if resource_id in price_dict:
                    price_value = price_dict[resource_id]
                    
                    if resource_name not in previous_prices:
                        previous_prices[resource_name] = None  # Initialize with None for the first iteration
                    
                    previous_price = previous_prices[resource_name]
                    
                    if previous_price is not None:
                        price_variation = ((price_value - previous_price) / previous_price) * 100
                      
                        min_variation_percentage = 10.0  # Minimum percentage change for triggering an alert

                        if abs(price_variation) >= min_variation_percentage:
                            change_type = "🟢" if price_variation > 0 else "🔴"
                            role_id = 1113455969557561415  # Replace with the actual role ID
                            mention_role = f"<@&{role_id}>"
                            embed = discord.Embed(title=f"🚨 Price Alert for {resource_name.capitalize()}",description=mention_role , color=discord.Color.red() if
                            any("🔴" in alert for alert in change_type) else discord.Color.green())
                            embed.set_footer(text="👑 Alert by ilyas_rifi 👑")

                            # Adding the image to the embed
                            resource_image_url = f"https://sunflower-land.com/play/erc1155/images/{resource_id}.png"
                            embed.set_thumbnail(url=resource_image_url)
                            
                            # Add fields for percentage change and price
                            embed.add_field(name="〽️ Percentage Change", value=f"`{abs(price_variation):.2f}%` {change_type}", inline=True)
                            embed.add_field(name="🏷️ Price", value=f"`{price_value:.4f}`", inline=True)
                            
                            channel_id = 1114900320955420696
                            channel = bot.get_channel(channel_id)
                            await channel.send(embed=embed)

                    previous_prices[resource_name] = price_value

        await asyncio.sleep(60)
        
bot.run('')