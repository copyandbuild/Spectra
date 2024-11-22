import discord
from discord.ext import commands
from discord.commands import slash_command

class maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Wartungen haha")
    @discord.guild_only()
    async def maintenance(self, ctx):
        if ctx.author.name != "lrrox":
            await ctx.respond("> Keine berechtigung", ephemeral=True)
            return

        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.CustomActivity(name="🛑 WARTUNGSARBEITEN 🛑"))
        await ctx.respond("done", ephemeral=True)

def setup(bot):
    bot.add_cog(maintenance(bot))

