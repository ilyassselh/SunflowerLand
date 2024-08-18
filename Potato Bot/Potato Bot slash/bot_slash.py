import discord
import requests
from discord import app_commands
from discord.ext import commands
import time
from datetime import datetime
from datetime import datetime, timezone, timedelta
import aiohttp
import math
import json
from collectible_list import *
from checkprice_fonction import *
import asyncio
from check_sell import *
from npc_price import npc


intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)

intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@bot.event
async def on_ready():
    global price_embed
    print(f"The bot has logged in as {bot.user}")
    
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.playing, 
        name="👑 made by ilyas_rifi 👑"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        
    except Exception as e:
        print(e)
  
        

@bot.tree.command(name="checksell", description="Check where is the best place to sell")
async def checksell(interaction: discord.Interaction, farm_id: str):
    await interaction.response.defer()

    async def background_task():
        try:
            resource_ids = {
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
                'wood': '601',
                'stone': '602',
                'iron': '603',
                'gold': '604',
                'egg': '605'
            }

            def format_price(price):
                parsed_value = float(price)
                factor = 10 ** 18
                reduction = 0.0294
                result = (parsed_value / factor) * (1 - reduction)
                return result

            def get_resource_id(resource_name):
                return resource_ids.get(resource_name.lower())

            def get_nifty_price(resource_id):
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
                    return None

                result = response.json()
                prices = result.get('prices', {})
                if resource_id in prices:
                    price = prices[resource_id]
                    return format_price(price)

                return None

            def get_goblin_price(sflitem_name):
                sfltools = requests.get('https://sfl.tools/api/listings/prices')
                sfltools_json = sfltools.json()

                for item in sfltools_json.values():
                    if item['sflItemName'].lower() == sflitem_name.lower():
                        return item['pricePerUnit']

                return None

            response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
            data = response.json()

            if 'state' in data and 'inventory' in data['state']:
                inventory = data['state']['inventory']
            else:
                await interaction.response.send_message("Invalid farm ID or data unavailable.")
                return

            crop_values = []

            for item, quantity in inventory.items():
                item_lower = item.lower()

                if item_lower in resource_ids:
                    resource_id = resource_ids[item_lower]
                    nifty_price = float(get_nifty_price(resource_id))
                    goblin_price = float(get_goblin_price(item_lower))

                    nifty_value = (float(quantity) - 0.3 * float(quantity)) * nifty_price
                    goblin_value = goblin_price * float(quantity)

                    crop_values.append({
                        'item': item.capitalize(),
                        'quantity': float(quantity),
                        'nifty_price': nifty_price,
                        'goblin_price': goblin_price,
                        'nifty_value': nifty_value,
                        'goblin_value': goblin_value
                    })

            embed = discord.Embed(title=f"🌿 Inventory Farm: {farm_id}", color=0x00ff00)
            total_farm_value_nifty = 0
            total_farm_value_goblin = 0

            for crop in crop_values:
                nifty_price_str = f"Price: {crop['nifty_price']:.2f} SFL"
                goblin_price_str = f"Price: {crop['goblin_price']:.2f} SFL"
                nifty_value_str = f"Sell: `{crop['nifty_value']:.2f} SFL`"
                goblin_value_str = f"Sell: `{crop['goblin_value']:.2f} SFL`"

                if crop['goblin_price'] != "N/A" and crop['goblin_price'] is not None:
                    num_lots = math.ceil(crop['quantity'] / 1000)
                    tax_amount = num_lots * 0.35
                    goblin_value_str += f"\nLots: `{num_lots}`"
                    goblin_value_str += f"\nTotal taxes: `{tax_amount:.2f} MATIC`"

                crop_info = (
                    f"**{crop['item']}**: ``{crop['quantity']:.0f}``\n"
                    f"**Niftyswap**\n"
                    f"{nifty_price_str}\n"
                    f"{nifty_value_str}\n"
                    f"**Goblin Trade**\n"
                    f"{goblin_price_str}\n"
                    f"{goblin_value_str}\n"
                )

                embed.add_field(name=f"\u200b", value=crop_info, inline=True)
                total_farm_value_nifty += crop['nifty_value']
                total_farm_value_goblin += crop['goblin_value']

            total_value_str_nifty = f"Total Farm Value (Niftyswap): {total_farm_value_nifty:.2f} SFL"
            total_value_str_goblin = f"Total Farm Value (Goblin Trade): {total_farm_value_goblin:.2f} SFL"
            total_value_str = f"```{total_value_str_nifty}\n{total_value_str_goblin}```"

            embed.add_field(name=f"Total Farm Value", value=total_value_str, inline=False)
            embed.set_footer(text=f"\n 👑 made by ilyas_rifi 👑")
            await interaction.followup.send(embed=embed)

        except Exception as e:
            error_message = "An error occurred while processing your request."
            await interaction.followup.send(error_message)

    # Exécutez la tâche en arrière-plan de manière asynchrone
    bot.loop.create_task(background_task())
    
    
    # Nombre d'entrées par page
ENTRIES_PER_PAGE = 25

@bot.tree.command(name="getlist", description="Get the best holders for an item")
async def getlist(interaction: discord.Interaction, item: str):
    # Capitalize each word and replace spaces with %20
    formatted_item = " ".join([word.capitalize() for word in item.split()])
    formatted_item = formatted_item.replace(" ", "%20")

    url = f"http://83.150.217.29:1796/getlist/{formatted_item}"
    response = requests.get(url)

    if response.status_code != 200:
        error_text = (
            f"### **Erreur : Aucune donnée disponible pour l'item {item}**\n"
            "Try with ``sunflower`` or ``pumpkin_soup``"
        )
        embed = discord.Embed(description=error_text, color=0x00ff00)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await interaction.response.send_message(embed=embed)
        print(f"Erreur {response.status_code} lors de la requête à l'API.")
        return

    leaderboard_data = response.json()
    if not leaderboard_data:
        error_text = (
            f"### **Erreur : Aucune donnée disponible pour l'item {item}**\n"
            "Try with ``sunflower`` or ``pumpkin_soup``"
        )
        embed = discord.Embed(description=error_text, color=0x00ff00)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await interaction.response.send_message(embed=embed)
        return

    leaderboard_text = f"### **🥇 Best holders of {item.capitalize()}:**\n"

    # Limiter à afficher seulement les 30 premiers joueurs
    for i, entry in enumerate(leaderboard_data[:30], start=1):
        position = entry["position"]
        player_id = entry["farm_id"]
        item_count = entry["item_count"]

        # Construire le texte du leaderboard
        leaderboard_text += f"**#{position}** | Farm: `{player_id}` ({item_count} {item})\n"

    # Envoie la réponse
    embed = discord.Embed(description=leaderboard_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="rankitem", description="Get the rank of a farm for a specific item")
async def rankitem(interaction: discord.Interaction, item: str, farm_id: str):
    formatted_item = " ".join([word.capitalize() for word in item.split()])
    formatted_item = formatted_item.replace(" ", "%20")
    
    url = f"http://83.150.217.29:1796/getlist/{formatted_item}/{farm_id}"
    response = requests.get(url)

    if response.status_code != 200:
        error_text = (
            f"### **Error: No data available for the item {item} and farm {farm_id}**\n"
            "Make sure the item name is correct and try again."
        )
        embed = discord.Embed(description=error_text, color=0xff0000)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await interaction.response.send_message(embed=embed)
        print(f"Error {response.status_code} while making API request.")
        return

    rank_data = response.json()
    if not rank_data:
        error_text = (
            f"### **Error: No data available for the item {item} and farm {farm_id}**\n"
            "Make sure the item name is correct and try again."
        )
        embed = discord.Embed(description=error_text, color=0xff0000)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await interaction.response.send_message(embed=embed)
        return

    rank_text = f"### **🥇 Rank of Farm `{farm_id}` for Item `{item.capitalize()}`:**\n"
    rank_position = rank_data.get("position", "N/A")
    rank_count = rank_data.get("item_count", "N/A")

    rank_text += f"**Rank:** #{rank_position}\n"
    rank_text += f"**Item Count:** {rank_count} {item}\n"

    # Send the response
    embed = discord.Embed(description=rank_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ticket", description="Get the ticket leaderboard")
async def ticket(interaction: discord.Interaction):
    url = f"http://83.150.217.29:1796/getlist/Crow%20Feather"
    response = requests.get(url)

    if response.status_code != 200:
        error_text = (
            f"### **Erreur : Aucune donnée disponible pour ticket\n"
        )
        embed = discord.Embed(description=error_text, color=0x00ff00)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await interaction.response.send_message(embed=embed)
        print(f"Erreur {response.status_code} lors de la requête à l'API.")
        return

    leaderboard_data = response.json()

    leaderboard_text = f"### **🥇 Leaderboard of Ticket:**\n"

    # Limiter à afficher seulement les 30 premiers joueurs
    for i, entry in enumerate(leaderboard_data[:30], start=1):
        position = entry['position']
        player_id = entry["farm_id"]
        item_count = entry["item_count"]

        # Construire le texte du leaderboard
        leaderboard_text += f"**#{position}** | Farm: `{player_id}` ({item_count} Crow Feather)\n"

    # Envoie la réponse
    embed = discord.Embed(description=leaderboard_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rankticket", description="Get the rank of a farm for Crow Feather")
async def rankticket(interaction: discord.Interaction, farm_id: str):
    url = f"http://83.150.217.29:1796/getlist/Crow%20Feather/{farm_id}"
    response = requests.get(url)

    if response.status_code != 200:
        error_text = (
            f"### **Error: No data available for farm {farm_id}**\n"
        )
        embed = discord.Embed(description=error_text, color=0xff0000)
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await interaction.response.send_message(embed=embed)
        print(f"Error {response.status_code} while making API request.")
        return

    rank_data = response.json()

    rank_text = f"### **🥇 Rank of Farm `{farm_id}` for Crow Feather:**\n"
    rank_position = rank_data.get("position", "N/A")
    rank_count = rank_data.get("item_count", "N/A")

    rank_text += f"**Rank:** #{rank_position}\n"
    rank_text += f"**Crow Feather Count:** {rank_count} Crow Feather\n"

    # Send the response
    embed = discord.Embed(description=rank_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="checkprice", description="check the price of an item")
async def checkprice(interaction: discord.Interaction, resource_name: str):
    resource_price = get_nifty_price(resource_name)
    goblin_price = float(get_goblin_price(sflitem_name=resource_name))
    change_24h_response = requests.get('http://83.150.217.29:1799/fluctuations/24h')
    change_1h_response = requests.get('http://83.150.217.29:1799/fluctuations/1h')
    change_7d_response = requests.get('http://83.150.217.29:1799/fluctuations/7d')
    
    if change_24h_response.status_code and change_1h_response.status_code == 200:
        variations_24h = change_24h_response.json().get(resource_name, {}).get('percentage_change', 'N/A')
        variations_1h = change_1h_response.json().get(resource_name, {}).get('percentage_change', 'N/A')
    else:
        variations_24h = 'N/A'
        variations_1h = 'N/A'
    
    checkprice_text = f"** 🛒 Check price of {resource_name.capitalize()}** :\n"
    if resource_price is not None and goblin_price is not None:
        formatted_price = "{:.6f}".format(resource_price)
        npc_price = npc.get(resource_name.capitalize())
        goblin_format = "{:.6f}".format(goblin_price)
        
        if npc_price is not None and npc_price != 0:
            npc_price = float(npc_price)  # Convert npc_price to float
            coeff_nifty = resource_price / npc_price
            coeff_goblin = goblin_price / npc_price
            coeff_nifty_format = "{:.3f}".format(coeff_nifty)
            coeff_goblin_format = "{:.3f}".format(coeff_goblin)
        else:
            coeff_nifty = float('nan') if npc_price is None else float('inf')
            coeff_goblin = float('nan') if npc_price is None else float('inf')
            coeff_nifty_format = "{:.3f}".format(coeff_nifty)
            coeff_goblin_format = "{:.3f}".format(coeff_goblin)

        # Construire l'URL de l'image de la ressource
        resource_id = get_resource_id(resource_name)  # Remplacez cette fonction par votre logique pour obtenir l'ID de la ressource
        resource_image_url = f"https://sunflower-land.com/play/erc1155/images/{resource_id}.png"
        lot_price = float(goblin_price) * 1000  # Convert formatted_price to float and calculate lot price
        lot_price_str = "{:.3f}".format(lot_price)  # Format lot price as a string with limited decimal places

        # Créer l'embed avec l'image de la ressource
        embed = discord.Embed(color=0x00ff00)
        embed.set_thumbnail(url=resource_image_url)
        embed.title = checkprice_text
        embed.add_field(name="Prix `(NiftySwap)`:\n", value=f":moneybag: `{formatted_price}` SFL\n:money_with_wings: Coef: `{coeff_nifty_format}`\n\n 〽️ **Change**\n1h: `{variations_1h:.2f}%`\n 24h: `{variations_24h:.2f}%`", inline=True)
        embed.add_field(name="Prix `(Goblin Trade)`:\n", value=f":moneybag: `{goblin_format}` SFL\n*Price for 1000 :* `{lot_price_str}` SFL\n\n:money_with_wings: Coef: `{coeff_goblin_format}`", inline=True)
        embed.set_footer(text="👑 made by ilyas_rifi 👑")

        # Check the size of the embed and split if needed
        if len(embed) <= 6000:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("The embed size exceeds the limit. Try a shorter resource name.")
    else:
        await interaction.response.send_message(f"Impossible d'obtenir le prix pour la ressource '{resource_name}'")  
        
@bot.tree.command(name="ping", description="Ping of the bot")
async def ping(interaction: discord.Interaction):
    latency = bot.latency
    await interaction.response.send_message(f"Pong! Latency: {latency * 1000:.2f} ms")

@bot.tree.command(name="maze", description="Get your maze profile")
async def maze(interaction: discord.Interaction, farm_id: str):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')

    if response.status_code == 200:
        cornmaze_text = f"### **🍿 Corn maze profile for farm {farm_id}**\n\n"
        cornmaze_data = response.json().get('state', {}).get('witchesEve', {}).get('maze', {})

        for week, week_data in cornmaze_data.items():
            attempts = week_data.get('attempts', [])
            started_at_count = sum(1 for attempt in attempts if "startedAt" in attempt)
            claimed_ticket = week_data.get('claimedFeathers', {})
            high_score = week_data.get('highestScore', {})

            cornmaze_text += f"🌾 Week {week}:\n"
            cornmaze_text += f"🍃 Claimed Feathers: ``{claimed_ticket}``\n"
            cornmaze_text += f"🌽 Total attempts: ``{started_at_count}``\n"
            cornmaze_text += f"⚡ Highest score: ``{high_score}``\n\n"

        embed = discord.Embed(description=cornmaze_text, color=0x00ff00)
        embed.set_footer(text="\n\n👑 made by ilyas_rifi 👑")
        await interaction.response.send_message(embed=embed)
    else:
        await ctx.send(f"``{farm_id}`` non trouvée ou erreur d'API.")

@bot.tree.command(name="delivery", description="Show farm deliveries")
async def delivery(interaction: discord.Interaction, farm_id: str):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    data = response.json()

    if 'state' not in data:
        await interaction.response.send_message(f"Impossible de récupérer les informations pour {farm_id}.")
        return

    delivery = data['state'].get('delivery')
    inventory = {item: float(quantity) for item, quantity in data['state'].get('inventory', {}).items()}

    if not delivery:
        await interaction.response.send_message(f"Aucune livraison en cours pour {farm_id}.")
        return

    embed = discord.Embed(title=f"Delivery for {farm_id}", color=0x00ff00)

    for order in delivery.get('orders', []):
        from_npc = order.get('from', "N/A")
        from_npc_c = from_npc.capitalize()
        items_required = order.get('items', {})
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

        items_list = "\n".join([f"{quantity}x {item}" for item, quantity in items_required.items()])

        delivery_text = f"**{from_npc_c}**\nStatus : {status}\n"
        delivery_text += f"`{datetime.fromtimestamp(order.get('readyAt', 0) // 1000).strftime('%d %b %Y %H:%M')} => dans {remaining_time}`\n"
        delivery_text += f"Need : {items_list}\n"

        if tickets is not None:
            delivery_text += f"Reward : {tickets} tickets\n"
        if sfl is not None:
            delivery_text += f"Reward : {sfl} SFL\n"

        embed.add_field(name="", value=delivery_text, inline=True)

    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="checknft", description="Show farm NFTs")
async def checknft(interaction: discord.Interaction, farm_id: str):
    response = requests.get(f"https://api.sunflower-land.com/visit/{farm_id}")
    farm_data = response.json()["state"]["inventory"]

    nft_text = f"### **Check NFTs for farm {farm_id}**\n"

    for item, quantity in farm_data.items():
        if item in nft_to_display:
            nft_text += f"`{item}`: `{quantity}`\n"

    embed = discord.Embed(description=nft_text, color=0x00ff00)
    embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="showquest", description="See the current task of a farm")
async def quest(interaction: discord.Interaction, farm_id: str):
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
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"Impossible de récupérer les quêtes pour {farm_id}.")

@bot.tree.command(name="checkharvest", description="Show the current harvest of a farm")
async def checkharvest(interaction: discord.Interaction, farm_id: str):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    response_json = response.json()
    
    crop_totals = {}
    trees_totals = 0
    stone_total = 0
    iron_total = 0
    gold_total = 0
    fruit_totals = {}
    
    crow_feather_total = 0  # Initialize the total Crow Feather count
        
    checkharvest_text = f"### **🏝️ Check harvest {farm_id}:**\n\n"
    has_crops = 'crops' in response_json['state']
    if not has_crops:
        await interaction.response.send_message(f"Farm {farm_id} is not planting.")
        return
    else:
        for crop_id, crop_data in response_json['state']['crops'].items():
            crop_name = crop_data['crop']['name']
            crop_amount = crop_data['crop']['amount']
            crop_totals[crop_name] = crop_totals.get(crop_name, 0) + crop_amount

            if "reward" in crop_data['crop'] and crop_data['crop']['reward']['items'][0]['name'] == "Crow Feather":
                reward_item_amount = crop_data['crop']['reward']['items'][0]['amount']
                crow_feather_total += reward_item_amount

        for crop_name, total_amount in crop_totals.items():
            checkharvest_text += f"**🌱 Crops**: `{total_amount:.2f}x`**{crop_name}**\n\n"
        
        checkharvest_text += f"**🦅 Reward**: `{crow_feather_total}x`**Crow Feather**\n\n"
        
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
    embed.set_footer(text="👑 made by ilyas_rifi 👑")
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name="showxp", description="Get the current value of food")
async def getxp(interaction: discord.Interaction, farm_id: str):
    response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')
    data = response.json()

    if "error" in data:
        await interaction.response.send_message(f"La ferme {farm_id} n'existe pas")
    else:
        response = requests.get(f'https://api.sunflower-land.com/visit/{farm_id}')

        food = data["state"]["inventory"]

        for item, quantity in food.items():
            if item in food_to_display:
                inventaire = (f"{item}: {quantity}")
        
        xp_values = [
            3, 24, 96, 90, 400, 56, 10, 1250, 250, 170, 290, 500, 255, 480, 170, 240,
            50, 2500, 2500, 225, 525, 650, 625, 750, 860, 1250, 1190, 1300, 1200,
            1100, 720, 760, 720, 730, 380, 250, 500, 1000, 500, 375, 310, 775, 975
        ]
        
        farm_recipes = enumerate(food_to_display)
        total_xp = 0

        skills = data["state"]["bumpkin"]["previousSkills"]
        observatoire = data["state"]["inventory"]

        boost_skills = "Kitchen Hand"
        boost_items = "Observatory"

        if boost_skills in skills and boost_items in observatoire:
            xp_values = [x * 1.1 for x in xp_values]  # Augmentation de 10% des valeurs de xp_values
        elif boost_skills in skills or boost_items in observatoire:
            xp_values = [x * 1.05 for x in xp_values]  # Augmentation de 5% des valeurs de xp_values

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
            description=response_text,
            color=0x00ff00
        )
        embed.set_footer(text="\n 👑 made by ilyas_rifi 👑")
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="checksfl", description="Check farm SFL value")
async def checksfl(interaction: discord.Interaction, farm_id: str):
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
    await interaction.response.send_message(embed=embed) 

bot.run("")