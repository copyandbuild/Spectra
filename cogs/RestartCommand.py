import asyncio

import discord
from discord.ext import commands
from discord.commands import slash_command
import os
import sys

class RestartCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="restart", description="Startet den Bot neu.")
    @commands.is_owner()
    async def restart(self, ctx):

        await ctx.respond("🔄 Der Bot wird neu gestartet...")
        try:
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            await ctx.respond(f"❌ Fehler beim Neustart: {e}")
            raise e

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name="Spectra wird gerade neugestartet..."))
        await asyncio.sleep(5)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="🔧 LΛRRΘΧ'S UTILITY ROBOT"))

def setup(bot):
    bot.add_cog(RestartCommand(bot))
