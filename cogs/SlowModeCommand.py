import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import ezcord

class Slowmode(ezcord.Cog, emoji="🔨", name="Slowmode", description="Hallo!"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description='Setze den SlowMode im Channel')
    @commands.has_permissions(manage_messages=True)
    @discord.guild_only()
    async def slowmode(self, ctx, seconds: Option(int, "› Slowmode in Sekunden", required=True)):
        if seconds < 0 or seconds > 21600:
            await ctx.respond("> Slowmode muss zwischen `0` und `21600` (6h) liegen", ephemeral=True)
            return

        if ctx.guild.me.guild_permissions.manage_channels:
            await ctx.channel.edit(slowmode_delay=seconds, reason=f"{ctx.author.name} run command slowmode")
            await ctx.respond(f"> Slowmode auf `{seconds}` Sekunden gesetzt.", ephemeral=True)
        else:
            await ctx.respond("> Der Bot hat keine Berechtigung, den Slowmode zu ändern.", ephemeral=True)

    @ezcord.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith(">slowmode"):
            if not message.author.guild_permissions.manage_messages:
                await message.reply("> Du hast keine Berechtigung, den Slowmode zu ändern.")
                return

            try:
                _, seconds = message.content.split()
                seconds = int(seconds)

                if seconds < 0 or seconds > 21600:
                    await message.reply("> Slowmode muss zwischen `0` und `21600` (6h) liegen")
                    return

                if message.guild.me.guild_permissions.manage_channels:
                    await message.channel.edit(slowmode_delay=seconds, reason=f"{message.author.name} run command slowmode")
                    await message.reply(f"> Slowmode auf `{seconds}` Sekunden gesetzt.")
                else:
                    await message.reply("> Der Bot hat keine Berechtigung, den Slowmode zu ändern.")
            except ValueError:
                await message.reply("> Bitte gib die Slowmode-Dauer in Sekunden an. Beispiel: `>slowmode 10`")

def setup(bot: commands.Bot):
    bot.add_cog(Slowmode(bot))
