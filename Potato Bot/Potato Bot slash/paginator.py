import discord
from discord.ext import commands
from discord import app_commands
from collections import deque
from typing import List
import requests

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

class PaginatorView(discord.ui.View):
    def __init__(self, pages: List[discord.Embed]):
        super().__init__(timeout=180)
        self.pages = pages
        self.index = 0
        self.message = None

    async def update_embed(self):
        embed = self.pages[self.index]  # Utilisez 'self.pages' au lieu de 'self.embeds'
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = False

        if self.index == 0:
            self.children[0].disabled = True

        if self.index == len(self.pages) - 1:
            self.children[1].disabled = True

        await self.message.edit(embed=embed, view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary)
    async def prev_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index = max(0, self.index - 1)
        await self.update_embed()

    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary)
    async def next_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.index = min(len(self.pages) - 1, self.index + 1)
        await self.update_embed()


@bot.tree.command(name="getlist", description="Get the best holders for an item")
async def getlist(interaction: discord.Interaction, item: str):
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

    pages = []
    for i in range(0, len(leaderboard_data), 30):
        embed = discord.Embed(title=f"🥇 Best holders of {formatted_item.capitalize()}:")
        for entry in leaderboard_data[i:i+30]:
            position = entry["position"]
            player_id = entry["farm_id"]
            item_count = entry["item_count"]
            embed.add_field(name=f"#{position} Farm: `{player_id}`", value=f"{item_count} {formatted_item}", inline=False)
        pages.append(embed)

    paginator_view = PaginatorView(pages)
    message = await interaction.response.send_message(embed=pages[0], view=paginator_view)
    paginator_view.message = message 




    
bot.run("")