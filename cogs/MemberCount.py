import discord
from discord.ext import commands, tasks
from discord.commands import slash_command

class MemberCountCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_member_count.start()

    @tasks.loop(minutes=5)
    async def update_member_count(self):
        guild = self.bot.get_guild(1253596135558479902)
        channel = guild.get_channel(1309258990290731129)
        member_count = sum(1 for member in guild.members if not member.bot)
        await channel.edit(name=f"〣│👤・{member_count} Mitglieder")

    @slash_command()
    @commands.has_permissions(administrator=True)
    async def force_update_member_count(self, ctx):
        await self.update_member_count()
        await ctx.respond("Mitgliederanzahl wurde manuell aktualisiert.", ephemeral=True)

    @update_member_count.before_loop
    async def before_update_member_count(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.update_member_count.cancel()

def setup(bot):
    bot.add_cog(MemberCountCog(bot))
