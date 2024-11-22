import discord
import ezcord
import json

bot = ezcord.Bot(intents=discord.Intents.all(),
                 activity=discord.CustomActivity(name="🔧 LΛRRΘΧ'S UTILITY ROBOT"),debug_guilds=["1253596135558479902"],
                 owner_id="1143510845368832111")

with open('token.json', 'r') as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

bot.load_cogs()
bot.run(TOKEN)