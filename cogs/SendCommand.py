import discord
from discord.ext import commands
from discord.commands import slash_command, Option, SlashCommandGroup
import ezcord

class SendCommand(ezcord.Cog, name="Send"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    send = SlashCommandGroup("send", default_member_permissions=discord.Permissions(administrator=True))

    @send.command(description='Sende eine Nachricht als Bot')
    @discord.guild_only()
    async def message(self, ctx, nachricht: Option(str, "› Das, was gesendet werden soll", required=True)):
        if ctx.author.guild_permissions.administrator:
            sucsessfull_embed = discord.Embed(
                title="✅ Nachricht Gesendet! ✅",
                description=f"Nachricht:\n```yml\n{nachricht}\n```",
                color=discord.Color.green()
            )
            await ctx.respond(embed=sucsessfull_embed, ephemeral=True, delete_after=3)
            await ctx.send(nachricht)
            return

        failed_embed = discord.Embed(
            title="⚠ Du hast keine rechte auf diesen befehl! ⚠",
            description="",
            color=discord.Color.red()
            )
        await ctx.respond(embed=failed_embed, ephemeral=True, delete_after=3)

    @send.command(description="Sende ein Embed als Bot")
    @discord.guild_only()
    async def embed(self, ctx):
        if ctx.author.guild_permissions.administrator:
            modal = EmbedModal(title="Erstelle ein Embed", timeout=None, custom_id="EmbedModalID")
            await ctx.send_modal(modal)

    @send.command(description='Sende eine Nachricht per DM')
    @discord.guild_only()
    async def dm(self, ctx,
                 empfänger: Option(discord.User, description="Der Nutzer, an Den die nachricht gehen soll",
                                   required=True),
                 nachricht: Option(str, description="Die Nachricht, Die an den Nutzer gesendet werden soll",
                                   required=True),
                 unbekannt: Option(bool, description="Soll Die nachricht deinen namen anzeigen?", required=False)):
        if ctx.author.guild_permissions.administrator:
            try:
                if unbekannt is False:
                    await empfänger.send(f'{nachricht}\n\nNachricht von: `{ctx.author}`')
                    await ctx.respond(
                        f'`{nachricht}` wurde erfolgreich an {empfänger.mention} gesendet.\nUnbekannt: `❌`',
                        ephemeral=True)
                else:
                    await empfänger.send(f'{nachricht}')
                    await ctx.respond(
                        f'`{nachricht}` wurde erfolgreich an {empfänger.mention} gesendet.\nUnbekannt: `✅`',
                        ephemeral=True)

            except discord.Forbidden as e:
                await ctx.respond(f'Ich kann dem ausgewählten Nutzer keine DM senden. \nError: {e}', ephemeral=True)
        else:
            embed = discord.Embed(
                title="⚠ Du hast keine Rechte auf diesen Befehl! ⚠",
                description=f"`{ctx.author.id}` missing permissions `administrator`!",
                color=discord.Color.dark_red()
            )
            await ctx.respond(embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(SendCommand(bot))

class EmbedModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Embed Titel",
                placeholder="Die Welt-Herrschaft übernehmen"
            ),
            discord.ui.InputText(
                label="Embed Beschreibung",
                placeholder="Als erstes überfallen wir jemanden...",
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Farbe",
                placeholder="Name z.b Blau, Grün...",
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction):
        colorline = self.children[2].value.lower()

        color_map = {
            "grün": discord.Color.green(),
            "blau": discord.Color.blue(),
            "lila": discord.Color.purple(),
            "pink": discord.Color.magenta(),
            "gelb": discord.Color.gold(),
            "weiß": discord.Color.lighter_grey(),
            "grau": discord.Color.light_grey(),
            "schwarz": discord.Color.dark_grey(),
            "rot": discord.Color.red(),
            "orange": discord.Color.orange(),
            "dunkel orange": discord.Color.dark_orange(),
            "embed": discord.Color.blurple()
        }

        if any(color_name in colorline for color_name in color_map):
            for key, value in color_map.items():
                if key in colorline:
                    color = value
                    break
        else:
            color = discord.Color.blurple()

        embed = discord.Embed(
            title=self.children[0].value,
            description=self.children[1].value,
            color=color
        )
        await interaction.response.send_message("POST Request send", delete_after=0, ephemeral=True)
        channel = interaction.channel
        await channel.send(embed=embed)