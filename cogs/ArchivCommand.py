import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import ezcord

class ArchivCommand(ezcord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Archiviere einen Kanal")
    @discord.default_permissions(manage_channels=True)
    async def archivieren(self, ctx, kanal: Option(discord.TextChannel,description="Wähle den Kanal aus, der archiviert werden soll",required=True)):
        kategorie = await self.bot.fetch_channel(1309258820916219904)

        if kanal.category_id == kategorie.id:
            await ctx.respond(f"{kanal.mention} ist bereits in der Kategorie {kategorie.mention}.", ephemeral=True)
            return

        try:

            await kanal.edit(category=kategorie)

            kanalembed = discord.Embed(
                title="LarroxUtils × Archivierung",
                description="`🔐` **Archiviert**\n- Dieser Kanal ist nun **archiviert** und nur für Administratoren sichtbar.",
                color=discord.Color.blue()
            )

            guild = await self.bot.fetch_guild(1253596135558479902)
            role = guild.get_role(1300983869969006624)

            await kanal.set_permissions(role, read_messages=False)

            await ctx.respond(f"> {kanal.mention} wurde erfolgreich nach {kategorie.mention} verschoben.", ephemeral=True)

            message_kanal = await kanal.send(embed=kanalembed)
            await message_kanal.pin()

            await kanal.purge(limit=1)

        except Exception as e:
            await ctx.respond(f"Ein Fehler ist aufgetreten: {str(e)}", ephemeral=True)


def setup(bot):
    bot.add_cog(ArchivCommand(bot))
