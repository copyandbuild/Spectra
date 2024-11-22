import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord

class Voice(ezcord.Cog, emoji="🔊"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, user, old, new):
        if new.channel is not None and new.channel.id == "1309255880394412032":
            guild = user.guild
            channel_name = user.name + "'s channel"
            category = discord.utils.get(guild.categories, name="> Temporäres Kontrollzentrum")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False),
                user: discord.PermissionOverwrite(connect=True)
            }
            new_channel = await guild.create_voice_channel(channel_name, overwrites=overwrites, category=category)
            await user.move_to(new_channel)
        if old.channel is not None and old.channel.name == user.name + "'s channel" and old.channel.category.name == "> Temporäres Kontrollzentrum":
            if len(old.channel.members) == 0:
                await old.channel.delete()

def setup(bot: commands.Bot):
    bot.add_cog(Voice(bot))