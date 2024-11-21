import discord
from discord import app_commands
from discord.ext import commands
import requests

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Needed to manage roles for members

# Set up the bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Wikipedia API endpoint
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
VERIFIED_ROLE_ID = 1306943064782143519  # Replace with the actual role ID

# Event: On bot ready
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands with Discord
    print(f'Logged in as {bot.user}!')

# Slash Command: Check if a Wikipedia account exists and assign a role if verified
@bot.tree.command(name="checkwiki", description="Check if a Wikipedia account exists and get verified.")
async def checkwiki(interaction: discord.Interaction, username: str):
    # Call Wikipedia API to check if user exists
    params = {
        "action": "query",
        "list": "users",
        "ususers": username,
        "format": "json"
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()

    # Check if the user exists
    if 'missing' not in data['query']['users'][0]:
        # Wikipedia account exists, assign the "Verified" role
        guild = interaction.guild
        member = interaction.user
        role = guild.get_role(VERIFIED_ROLE_ID)

        if role:
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention}, your Wikipedia account '{username}' has been verified! Role assigned.")
        else:
            await interaction.response.send_message("The specified role does not exist. Please check the role ID.")
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, the Wikipedia account '{username}' does not exist.")

# Run the bot with your token
bot.run("TOKEN")  # Replace with your bot's token


