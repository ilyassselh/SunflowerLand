import discord
from discord.ext import commands
import requests
import json
import aiohttp
import time
from datetime import datetime

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True

bot = commands.AutoShardedBot(
    command_prefix="!",
    intents=intents,
    description="__Bot by ilyas_rifi__👑\nhttps://discord.gg/TBPBmuvT\n\n**Support me**\n||``0x5a3adc9b55fa907809e7347fe9bfdecff2fdf55d``||"
)


@bot.event
async def on_ready():
  print(f"Bot is ready. Logged in as {bot.user.name}")

redirection_channel_id = 1125521291601002667

@bot.event
async def on_message(message):
    if message.author == bot.user:
        # Ignorez les messages provenant du bot lui-même
        return

    if isinstance(message.channel, discord.DMChannel):
        # Si le message provient d'un DM, redirigez-le vers le canal spécifié
        redirection_channel = bot.get_channel(redirection_channel_id)
        if redirection_channel:
            embed_text = f"### User:\n **{message.author}** **->** ***{message.content}***"
            embed = discord.Embed(description=embed_text ,color=0x00ff00)
            embed.set_footer(text = "\n 👑 made by ilyas_rifi 👑")
            await redirection_channel.send(embed=embed)
        else:
            print(f"Canal de redirection introuvable. Vérifiez l'ID du canal : {redirection_channel_id}")

        return

    await bot.process_commands(message)

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online,
                            activity=discord.Activity(
                              type=discord.ActivityType.playing,
                              name="👑 made by ilyas_rifi 👑"))
@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send(f"Pong! Latency: {latency * 1000:.2f} ms")
    
@bot.command()
async def maze(ctx, farm_id):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    if response.status_code == 200:
        cornmaze_text = f"### **🍿 Corn maze profile for farm {farm_id}**\n\n"
        cornmaze_data = response.json().get('state', {}).get('witchesEve', {}).get('maze', {}).get('1', {})
        attempts = cornmaze_data.get('attempts', [])
        started_at_count = sum(1 for attempt in attempts if "startedAt" in attempt)
        claimed_ticket = cornmaze_data.get('claimedFeathers', {})
        high_score = cornmaze_data.get('highestScore', {})

        cornmaze_text += f"🍃 Claimed Feathers : ``{claimed_ticket} ``\n\n🌽 Total attempts : ``{started_at_count}``\n\n⚡ Highest score : ``{high_score}``\n"
        
        embed = discord.Embed(description=cornmaze_text, color=0x00ff00)
        embed.set_footer(text="\n\n 👑 made by ilyas_rifi 👑")
        await ctx.channel.send(embed=embed)
    else:
        await ctx.send(f"``{farm_id}`` non trouvée ou erreur d'API.")    


@bot.command()
async def getlist(ctx, item):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://ticket.trackers.vip/api/getlist/{item}"
        ) as response:
            leaderboard_data = await response.json()

    if not leaderboard_data:
        error_text = (
            f"### **Erreur : Aucune donnée disponible pour l'item {item}**\n"
            "Try with ``sunflower`` or ``pumpkin_soup``"
        )
        embed = discord.Embed(description=error_text, color=0x00ff00)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await ctx.channel.send(embed=embed)
        return

    leaderboard_text = f"### **🥇 Best holders of {item}:**\n"

    for rank in leaderboard_data[:30]:
        position = rank["position"]
        player_id = rank["playerId"]
        item_count = rank["itemCount"]
        leaderboard_text += f"\n**#{position}** | Farm: `{player_id}` ({item_count} {item})"

    embed = discord.Embed(description=leaderboard_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)


@bot.command()
async def ticket(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://83.150.217.29:5000/rank"
        ) as response:
            leaderboard_data = await response.json()

    leaderboard_text = "### **🏆 Leaderboard ticket : **\n"

    for rank in leaderboard_data[:30]:
        position = rank["position"]
        farm = rank["farm_id"]
        ticket_count = rank["crow_feather_count"]
        leaderboard_text += f"**#{position}** | Farm : `{farm}` ({ticket_count} tickets)\n"

    embed = discord.Embed(description=leaderboard_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)


@bot.command()
async def checknft(ctx, farm_id):
    response = requests.get(f"https://api.sunflower-land.com/visit/{farm_id}")
    check = response.json()["state"]["inventory"]

    nft_to_display = [
    "Christmas Tree", "Hoot", "Angel Bear", "Kuebiko", "Foreman Beaver",
    "Russian Flag", "Farm Cat", "Ukrainian Flag", "Iron Idol", "Turkish Flag",
    "Gold Egg", "Chicken Coop", "Mysterious Parsnip", "Nugget", "Indian Flag",
    "Farm Dog", "Apprentice Beaver", "Black Berry", "Cabbage Girl",
    "American Flag", "Rainbow Artist Bear", "Sunflower Rock", "Carrot Sword",
    "Heart of Davy Jones", "Wood Nymph Wendy", "Scarecrow", "Argentinian Flag",
    "Rock Golem", "Squirrel Monkey", "Gnome", "Woody the Beaver",
    "Rocky the Mole", "Peeled Potato", "Blossom Tree", "Ayam Cemani",
    "Rooster", "Cabbage Boy", "Undead Rooster", "French Flag", "Goblin Flag",
    "Rich Bear", "Chinese Flag", "Mysterious Head", "Lady Bug", "Nancy",
    "Tunnel Mole", "Observatory", "Pirate Flag", "Lunar Calendar",
    "Sunflower Flag", "Classy Bear", "Egg Basket", "Nyon Statue",
    "Sunflower Statue", "Blue Egg", "Red Egg", "Victoria Sisters", "Pink Egg",
    "Purple Egg", "Maneki Neko", "Tiki Totem", "Palm Tree", "Sunflower Bear",
    "Giant Carrot", "Valentine Bear", "Pablo The Bunny", "Homeless Tent",
    "Rich Chicken", "Speed Chicken", "Sunflowerr Tombstone", "Christmas Bear",
    "Fat Chicken", "Flamingo", "Karkinos", "Goblin Crow", "Collectible Bear",
    "Cyborg Bear", "Easter Bunny", "Wicker Man", "Christmas Snow Globe",
    "Farmer Bath", "Easter Bear", "Fountain", "War Tombstone", "Potato Statue",
    "War Skull", "Heart Balloons", "Beach Ball", "Easter Bush",
    "Golden Bonsai", "Badass Bear", "Brilliant Bear", "Chef Bear",
    "Construction Bear", "Farmer Bear", "Whale Bear", "T-Rex Skull",
    "Pirate Bear", "Abandoned Bear", "Algerian Flag", "Australian Flag",
    "Basic Bear", "Basic Scarecrow", "Belgian Flag", "Bonnie's Tombstone",
    "Brazilian Flag", "British Flag", "Obie", "Maximus", "Purple Trail", "Green Amulet", 
    "Beetroot Amulet", "Carrot Amulet", "Sunflower Amulet", "Angel Wings", 
    "Sunflower Shield", "Eggplant Onesie"
    ]

    checknft_text = f"### **Check NFT farm: {farm_id}**\n"

    for item, quantity in check.items():
        if item in nft_to_display:
            checknft_text += f"``{item}``: ``{quantity}``\n"

    embed = discord.Embed(description=checknft_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)


@bot.command()
async def checkfarm(ctx, farm_id):
    response = requests.get(f"https://api.sunflower-land.com/visit/{farm_id}")
    inventaire = response.json()["state"]["inventory"]

    checkfarm_text = f"### **🌿 Check inventory Farm: {farm_id}**\n"
    item_to_display = [
        "Sunflower",
        "Potato",
        "Pumpkin",
        "Carrot",
        "Cabbage",
        "Beetroot",
        "Cauliflower",
        "Parsnip",
        "Eggplant",
        "Radish",
        "Wheat",
        "Kale",
        "Blueberry",
        "Orange",
        "Apple",
        "Wood",
        "Stone",
        "Iron",
        "Gold",
        "Egg",
    ]

    for item, quantity in inventaire.items():
        if item in item_to_display:
            checkfarm_text += f"``{item}``: `{quantity}`\n"

    embed = discord.Embed(description=checkfarm_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)


@bot.command()
async def quest(ctx, farm_id):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    quest = response.json()['state']

    if response.status_code == 200:
        quest_text = f'### **🔍 Quêtes en cours pour {farm_id}**\n\n'

        chores = quest['chores']
        skipped_quest = chores['choresSkipped']
        completed_quest = chores['choresCompleted']
        quete_en_cours = chores['chores']

        for quest_id, data in quete_en_cours.items():
            activity = data['activity']
            description = data['description']
            requirement = data['requirement']
            tickets = data['tickets']
            completed_at = data.get('completedAt')
            
            quest_text += f"**{quest_id} - {description}**"

            if completed_at:
                 quest_text += " ✅\n"
            else :
                quest_text += " ❌\n"

            quest_text += f"`Reward` : ``🎁 {tickets} Crow Feather``\n\n"

        
        quest_text += f"```Completed quest {completed_quest} | Skipped quest {skipped_quest}```"
        embed = discord.Embed(description=quest_text, color=0x00ff00)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await ctx.channel.send(embed=embed)
    else:
        await ctx.send(f"Impossible de récupérer les quêtes pour {farm_id}.")
        
@bot.command()
async def delivery(ctx, farm_id):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    data = response.json()

    if 'state' not in data:
        await ctx.send(f"Impossible de récupérer les informations pour {farm_id}.")
        return

    delivery = data['state'].get('delivery')
    inventory = {item: float(quantity) for item, quantity in data['state'].get('inventory', {}).items()}

    if not delivery:
        await ctx.send(f"Aucune livraison en cours pour {farm_id}.")
        return

    embed = discord.Embed(title=f"Delivery for {farm_id}", color=0x00ff00)

    for order in delivery.get('orders', []):
        from_npc = order.get('from', "N/A")
        from_npc_c = from_npc.capitalize()
        items_required = order.get('items', {})

        if items_required:
            items_list = "\n".join([f"{quantity}x {item}" for item, quantity in items_required.items()])

            reward = order.get('reward', {})
            tickets = reward.get('tickets')
            sfl = reward.get('sfl')

            status = "❌"
            for item, quantity in items_required.items():
                if item in inventory and inventory[item] >= quantity:
                    status = "✅"
                else:
                    status = "❌"
                    break

            remaining_seconds = order.get('readyAt', 0) // 1000 - time.time()
            remaining_time = f"{int(remaining_seconds // 3600)} hours"

            delivery_text = f"**{from_npc_c}**\nStatus : {status}\n"
            delivery_text += f"`{datetime.fromtimestamp(order.get('readyAt', 0) // 1000).strftime('%d %b %Y %H:%M')} => dans {remaining_time}`\n"
            delivery_text += f"Need : {items_list}\n"

            if tickets is not None:
                delivery_text += f"Reward : {tickets} tickets\n"
            if sfl is not None:
                delivery_text += f"Reward : {sfl} SFL\n"

            embed.add_field(name="", value=delivery_text, inline=True)

    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.send(embed=embed)    
        

@bot.command()
async def checkharvest(ctx, farm_id):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    response_json = response.json()
    
    crop_totals = {}
    trees_totals = 0
    stone_total = 0
    iron_total = 0
    gold_total = 0
    fruit_totals = {}
        
    checkharvest_text = f"### **🏝️ Check harvest {farm_id}:**\n\n"
    has_crops = 'crops' in response_json['state']
    if not has_crops:
        await ctx.send(f"Farm {farm_id} is not planting.")
        return
    else :
        for crop_id, crop_data in response_json['state']['crops'].items():
            crop_name = crop_data['crop']['name']
            crop_amount = crop_data['crop']['amount']
            crop_totals[crop_name] = crop_totals.get(crop_name, 0) + crop_amount

        for crop_name, total_amount in crop_totals.items():
            checkharvest_text += f"**🌱 Crops**: `{total_amount:.2f}x`**{crop_name}**\n\n"
        
        for trees, trees_data in response_json['state']['trees'].items():
            trees_amount = trees_data['wood']['amount']
            trees_totals += trees_amount
    
        checkharvest_text += f"**🌳 Trees**:\n `{trees_totals:.2f}`**Woods**\n\n"
    
        for stone, stone_data in response_json['state']['stones'].items():
            stone_amount = stone_data['stone']['amount']
            stone_total += stone_amount
    
        checkharvest_text += f"**⛏️ Stones**:\n `{stone_total:.2f}`x**Stone**\n\n"
    
        for iron, iron_data in response_json['state']['iron'].items():
            iron_amount = iron_data['stone']['amount']
            iron_total += iron_amount
    
        checkharvest_text += f"**⛏️ Iron**:\n `{iron_total}`x**Iron**\n\n"
    
        for gold, gold_data in response_json['state']['gold'].items():
            gold_amount = gold_data['stone']['amount']
            gold_total += gold_amount
    
        checkharvest_text += f"**⛏️ Gold**:\n `{gold_total}`x**Gold**\n\n"
    
        for fruit_id, fruit_data in response_json['state']['fruitPatches'].items():
            fruit_name = fruit_data['fruit']['name']
            fruit_harvest = fruit_data['fruit']['harvestsLeft']
            fruit_totals[fruit_name] = fruit_totals.get(fruit_name, 0) + fruit_harvest

        for fruit_name, total_fruit_amount in fruit_totals.items():
            checkharvest_text += f"**🍉 Fruits harvestLeft**:\n `{total_fruit_amount:.2f}x`**{fruit_name}**\n\n"
    
    embed = discord.Embed(description=checkharvest_text, color=0x00ff00)
    embed.set_footer(text="🌟 Bot made by ilyas_rifi 🌟")
    await ctx.send(embed=embed)


@bot.command()
async def getxp(ctx, farm_id):
  response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
  data = response.json()

  if "error" in data:
    await ctx.send(f"La ferme {farm_id} n'existe pas")
  else:
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')

    food = data["state"]["inventory"]

    food_to_display = [
      "Mashed Potato", "Pumpkin Soup", "Bumpkin Broth", "Boiled Eggs",
      "Kale Stew", "Mushroom Soup", "Reindeer Carrot", "Kale Omelette",
      "Cabbers n Mash", "Roast Veggies", "Bumpkin Salad", "Goblin's Treat",
      "Cauliflower Burger", "Pancakes", "Club Sandwich",
      "Mushroom Jacket Potatoes", "Sunflower Crunch", "Bumpkin Roast",
      "Goblin Brunch", "Fruit Salad", "Sunflower Cake", "Potato Cake",
      "Pumpkin Cake", "Carrot Cake", "Cabbage Cake", "Beetroot Cake",
      "Cauliflower Cake", "Parsnip Cake", "Radish Cake", "Wheat Cake",
      "Mushroom Pie", "Honey Cake", "Kale & Mushroom Pie", "Orange Cake",
      "Blueberry Jam", "Fermented Carrots", "Sauerkraut", "Fancy Fries",
      "Apple Juice", "Orange Juice", "Purple Smoothie", "Power Smoothie",
      "Bumpkin Detox"
    ]

    xp_values = [
      3, 24, 96, 90, 400, 56, 10, 1250, 250, 170, 290, 500, 255, 480, 170, 240,
      50, 2500, 2500, 225, 525, 650, 625, 750, 860, 1250, 1190, 1300, 1200,
      1100, 720, 760, 720, 730, 380, 250, 500, 1000, 500, 375, 310, 775, 975
    ]

    for item, quantity in food.items():
      if item in food_to_display:
        inventaire = (f"{item}: {quantity}")

    farm_recipes = enumerate(food_to_display)
    total_xp = 0

    skills = data["state"]["bumpkin"]["previousSkills"]
    observatoire = data["state"]["inventory"]

    boost_skills = "Kitchen Hand"
    boost_items = "Observatory"

    if boost_skills in skills and boost_items in observatoire:
      xp_values = [x * 1.1 for x in xp_values
                   ]  # Augmentation de 10% des valeurs de xp_values
    elif boost_skills in skills or boost_items in observatoire:
      xp_values = [x * 1.05 for x in xp_values
                   ]  # Augmentation de 5% des valeurs de xp_values

    xp_text = ""
    for i, food_name in farm_recipes:
      quantity = int(food.get(food_name, 0))
      if quantity > 0:
        xp = xp_values[i]
        xp_total = xp * quantity
        total_xp += xp_total
        xp_format = "{:.1f}".format(xp_total)
        xp_text += f"**{food_name}** | `{quantity}` : {xp_format} XP\n"

    response_text = f"### **Le total d'XP pour la ferme {farm_id} est de : {total_xp} XP**\n\n"
    response_text += "**XP détaillé:**\n" + xp_text

    embed = discord.Embed(
      description=response_text ,
      color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)

@bot.command()
async def donate(ctx):
  donate_text = """### **💰 Help me to improve bot's quality :**\n\n
  **🦊 metamask :** ``0x5a3adc9b55fa907809e7347fe9bfdecff2fdf55d (for donations)``
  **🌻 SFL farm :** ``23771``
  **🥔 My own server :** ``https://discord.gg/ATqMX6deZr``
  ***⚡ The donations will be used to improve the speed of the bot (10$/month)***\n\n
  **🚀 Manafix server (`Bumpkins trackers, Bumpkins snipers and NiftySnipe`) :** ``https://discord.gg/avYr4BSXaT``
  *✨ Thanks to manafix who help me to retrieve some data ✨*
  """
  embed = discord.Embed(
      description=donate_text ,
      color=0x00ff00)
  embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
  await ctx.channel.send(embed=embed)
    
@bot.command()
async def howto(ctx):
  help_text = """**List of commands:**
    **!getlist** ``<item>``: Get the leaderboard for a specific item
    **!ticket**: Get the ticket leaderboard
    **!checknft** ``<farm_id>``: Check the NFTs of a farm
    **!checkfarm** ``<farm_id>``: Check the inventory of a farm
    **!checkprice** ``<ressource>`` : Check the price of a ressource
    **!quest** ``<farm_id>``: Show the current farm quest
    **!getxp** ``<farm_id>``: Check the xp value of your food
    **!auction** ``<x*ressource>``: Get the leaderboard of auction item
    **!rank** ``<farm_id>``: Get the rank of a farm
    **!sellnpc** ``<farm_id>``: Get the value of inventory at the NPC market
    **!checkharvest** ``<farm_id>``: Get farm information
    **!donate**: Give me some help
    **!howto**: Show this help message
    **!maze** ``farm_id``: Get your maze stats
    **!delivery** ``farm_id``: Get the next deliveries"""
  
  embed = discord.Embed(title="Bot Commands",
                        description=help_text,
                        color=0x00ff00)
  embed.set_footer(text = "\n 👑 made by ilyas_rifi 👑")
  await ctx.channel.send(embed=embed)


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

    if response.status_code != 200:
        print("Code erreur")
    else :
        result = response.json()
        prices = result['prices']
        if resource_id in prices:
            price = prices[resource_id]
            return format_price(price, 1)
        
def get_goblin_price(sflitem_name):
    sfltools = requests.get('https://sfl.tools/api/listings/prices')
    sfltools_json = sfltools.json()

    for item in sfltools_json.values():
        if item['sflItemName'].lower() == sflitem_name.lower():
            return item['pricePerUnit']
    
    return None
    
@bot.command()
async def checkprice(ctx, resource_name):
    resource_price = get_nifty_price(resource_name)
    goblin_price = get_goblin_price(sflitem_name=resource_name)
    checkprice_text = f"** 🛒 Check price of {resource_name}** :\n"
    if resource_price is not None and goblin_price is not None:
        formatted_price = "{:.2f}".format(resource_price)
        coefficient = float(resource_price) / float(goblin_price)

        # Construire l'URL de l'image de la ressource
        resource_id = get_resource_id(resource_name)  # Remplacez cette fonction par votre logique pour obtenir l'ID de la ressource
        resource_image_url = f"https://sunflower-land.com/play/erc1155/images/{resource_id}.png"
        lot_price = float(goblin_price) * 1000  # Convert formatted_price to float and calculate lot price
        lot_price_str = "{:.2f}".format(lot_price)  # Format lot price as a string with limited decimal places

        # Créer l'embed avec l'image de la ressource
        embed = discord.Embed(color=0x00ff00)
        embed.set_thumbnail(url=resource_image_url)
        embed.title = checkprice_text
        embed.add_field(name="Prix `(NiftySwap)`:\n", value=f":moneybag: `{formatted_price}` SFL", inline=False)
        embed.add_field(name="Prix `(Goblin Trade)`:\n", value=f":moneybag: `{goblin_price}` SFL\n*Price for 1000 :* `{lot_price_str}` SFL", inline=False)
        embed.add_field(name="Coefficient:", value=f":money_with_wings: `{coefficient:.6f}`", inline=False)
        embed.set_footer(text="👑 made by ilyas_rifi 👑")

        # Check the size of the embed and split if needed
        if len(embed) <= 6000:
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send("The embed size exceeds the limit. Try a shorter resource name.")
    else:
        await ctx.send(f"Impossible d'obtenir le prix pour la ressource '{resource_name}'")

@bot.command()
async def auction(ctx, *resources):
    url = 'https://ticket.trackers.vip/api/getAuctions/' + '%20'.join(resources)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await ctx.send("Erreur lors de la récupération des enchères.")
                return

            data = await response.json()

    auctions = data
    if not auctions:  # Vérifier si la liste des enchères est vide
        error_text = f"### No data\nTry with ``sunflower`` and ``pumpkin``"
        embed = discord.Embed(description=error_text, color=0x00ff00)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await ctx.channel.send(embed=embed)
        return

    auction_text = f"### **Leaderboard of auctions {' | '.join(resources)}:**\n"
    position_counter = 0

    for auction in auctions:
        position = auction['position']
        farm_id = auction['playerId']
        resource_values = [auction[resource] for resource in resources]
        auction_text += f"**#{position}** | Farm `{farm_id}`: "

        for resource, value in zip(resources, resource_values):
            auction_text += f"`{value} {resource}` | "

        auction_text = auction_text[:-3]  # Remove the extra " | " at the end
        auction_text += "\n"

        position_counter += 1
        if position_counter == 30:
            break

    embed = discord.Embed(description=auction_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)


@bot.command()
async def rank(ctx, farm_id):
    url = f'http://83.150.217.29:5000/rank/{farm_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await ctx.send(f"Il semble qu'il y ait une erreur pour la farm {farm_id}, mon gourmand.")
                return

            rank = await response.json()

    if 'rank' in rank and 'ticketNumber' in rank:
        rank_farm = rank['position']
        number_ticket = rank['crow_feather_count']

        rank_text = f"### **🥇 Rank ticket for farm : {farm_id}**\n"
        rank_text += f"#**{rank_farm}** | `{number_ticket} ticket`"
    else:
        await ctx.send(f"Il semble qu'il y ait une erreur pour la farm {farm_id}, mon gourmand.")
        return
    
    embed = discord.Embed(description=rank_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)

@bot.command()
async def sell(ctx, farm_id):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    inventory = response.json()['state']['inventory']

    def get_goblin_price(sflitem_name):
        sfltools = requests.get('https://sfl.tools/api/listings/prices')
        sfltools_json = sfltools.json()

        for i in sfltools_json.values():
            if i['sflItemName'].lower() == sflitem_name.lower():
                return float(i['pricePerUnit'])  # Convertir en nombre flottant

    checkfarm_lines = []
    item_to_display = [
        "Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot",
        "Cauliflower", "Parsnip", "Eggplant", "Radish", "Wheat", "Kale",
        "Blueberry", "Orange", "Apple", "Wood", "Stone", "Iron", "Gold", "Egg",
    ]

    total_value = 0  # Valeur totale de l'inventaire
    total_lots = 0  # Nombre total de lots nécessaires
    total_taxes = 0  # Taxes totales à payer

    for item, quantity in inventory.items():
      if item in item_to_display:
        price = get_goblin_price(item)
        
        if price is not None:  # Vérifier si le prix est valide
            total_price = float(quantity) * price
            total_price_str = "{:.2f}".format(total_price)  # Formater le prix avec deux décimales
            total_value += total_price

            lots_needed = (float(quantity) + 499) // 500
            total_lots += lots_needed

            taxes = lots_needed * 0.25
            total_taxes += taxes
            taxes_str = "{:.2f}".format(taxes)  # Formater les taxes avec deux décimales

            line = f"**{item}** | `{quantity}` : `{total_price_str} SFL` \n``Total Lot: {lots_needed}, Taxes: {taxes_str} MATIC``\n"
            checkfarm_lines.append(line)
        else:
            line = f"**{item}** | `{quantity}` : Prix non disponible\n"
            checkfarm_lines.append(line)


    checkfarm_text = "### **💵 Check sell inventory Farm: {}**\n".format(farm_id)
    checkfarm_text += "\n".join(checkfarm_lines)

    total_value_formatted = "{:.2f}".format(total_value)  # Formater la valeur totale avec deux décimales
    total_taxes_formatted = "{:.2f}".format(total_taxes)  # Formater les taxes totales avec deux décimales

    summary = f"```Total Value: {total_value_formatted} SFL```\n"
    summary += f"```Total Lots Needed: {total_lots}```\n"
    summary += f"```Total Taxes: {total_taxes_formatted} MATIC```"

    embed = discord.Embed(
        description=checkfarm_text + "\n" + summary,
        color=0x00ff00
    )
    embed.set_footer(text="👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)

market_prices = {
    "resources": [
        {
            "name": "Sunflower",
            "code": 201,
            "price": 0.00025
        },
        {
            "name": "Potato",
            "code": 202,
            "price": 0.00175
        },
        {
            "name": "Pumpkin",
            "code": 203,
            "price": 0.005
        },
        {
            "name": "Carrot",
            "code": 204,
            "price": 0.01
        },
        {
            "name": "Cabbage",
            "code": 205,
            "price": 0.01875
        },
        {
            "name": "Beetroot",
            "code": 206,
            "price": 0.035
        },
        {
            "name": "Cauliflower",
            "code": 207,
            "price": 0.053125
        },
        {
            "name": "Parsnip",
            "code": 208,
            "price": 0.08125
        },
        {
            "name": "Radish",
            "code": 209,
            "price": 0.11875
        },
        {
            "name": "Wheat",
            "code": 210,
            "price": 0.0875
        },
        {
            "name": "Wood",
            "code": 601,
            "price": 0
        },
        {
            "name": "Stone",
            "code": 602,
            "price": 0
        },
        {
            "name": "Iron",
            "code": 603,
            "price": 0
        },
        {
            "name": "Gold",
            "code": 604,
            "price": 0
        },
        {
            "name": "Egg",
            "code": 605,
            "price": 0
        },
        {
            "name": "Kale",
            "code": 211,
            "price": 0.125
        },
        {
            "name": "Blueberry",
            "code": 213,
            "price": 0.15
        },
        {
            "name": "Orange",
            "code": 214,
            "price": 0.225
        }
    ]
}

@bot.command()
async def sellnpc(ctx, farm_id):
    response = requests.get(f"https://api.sunflower-land.com/visit/{farm_id}")
    inventory = response.json()["state"]["inventory"]
    balance = response.json()["state"]["balance"]
    
    items_to_display = ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Eggplant", "Radish", "Wheat", "Kale", "Blueberry", "Orange", "Apple", "Wood", "Stone", "Iron", "Gold", "Egg", "Axe"]
    
    total_value = 0
    price_text = f"### **💵 Check sell inventory Farm: {farm_id}**\n"
    
    for item, quantity in inventory.items():
     if item in items_to_display:
        for resource in market_prices['resources']:
            if resource['name'] == item:
                price_market = resource['price']
                each_resource_price = float(price_market) * float(quantity)
                total_value += each_resource_price
                nom_ressource = resource['name']
                total_value_text = f"```Total Value : {total_value:.2f} SFL```"
                price_text += f"**{item}** | `{float(quantity):.2f}` : `{each_resource_price:.2f} SFL`\n"
                break
        else:
            each_resource_price = 0
    
    embed = discord.Embed(
        description= price_text + "\n" + total_value_text,
        color=0x00ff00
    )
    embed.set_footer(text="👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed)
    
@bot.command()
async def checksfl(ctx, farm_id):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    res = response.json()
    sfl_balance = float(res['state']['balance'])

    check_balance_text = f"### **💶 Check balance of {farm_id}:**\n"
    check_balance_text += f"``{sfl_balance:.2f}x``**SFL**\n\n"

    if sfl_balance <= 10:
        withdraw_tax = 0.7
        sfl_balance *= withdraw_tax
        check_balance_text += f"```SFL after withdraw: {sfl_balance:.2f}🌻```"
    elif sfl_balance <= 100:
        withdraw_tax = 0.75
        sfl_balance *= withdraw_tax
        check_balance_text += f"```SFL after withdraw: {sfl_balance:.2f}🌻```"
    elif sfl_balance <= 1000:
        withdraw_tax = 0.80
        sfl_balance *= withdraw_tax
        check_balance_text += f"```SFL after withdraw: {sfl_balance:.2f}🌻```"
    elif sfl_balance <= 5000:
        withdraw_tax = 0.85
        sfl_balance *= withdraw_tax
        check_balance_text += f"```SFL after withdraw: {sfl_balance:.2f}🌻```"
    elif sfl_balance <= 10000:
        withdraw_tax = 0.90
        sfl_balance *= withdraw_tax
        check_balance_text += f"```SFL after withdraw: {sfl_balance:.2f}🌻```"

    embed = discord.Embed(
        description=check_balance_text,
        color=0x00ff00
    )
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await ctx.channel.send(embed=embed) 


bot.run("")
