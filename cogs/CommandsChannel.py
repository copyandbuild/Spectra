import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, SlashCommandGroup
from discord.ui import Button, View
import ezcord
from ezcord import Bot, emb

class CommandsChannel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    class KeksKnopf(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Cookie Hosting", style=discord.ButtonStyle.green, emoji="<:codingkeks_cookie:1296197308643414027>", custom_id="keks")
        async def callback(self, button: discord.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f"Fast all Unsere Bots laufen auf [Cookie-Hosting](https://cookieapp.me/)", ephemeral=True)

    @ezcord.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(self.KeksKnopf())

    @slash_command(description="Der Command um das Embed für den Bot Command Channel zu senden")
    async def commands(self, ctx: discord.ApplicationContext):

        guild = ctx.guild

        embed = discord.Embed(
            title=f"{guild.name} - :wrench: Commands",
            description="Hier findest du eine liste an hilfreichen Commands die du nutzen kannst, um z.b Musik zu hören, Minispiele zu spielen oder anderes, tob dich ruhig aus, alle nachrichten werden hier nach `2 Minuten` gelöscht.",
            color=discord.Color.green()
        )
        embed.add_field(name="</minispiel 8ball:1295784185717592104>",
                        value="> Stelle der :sparkles: Magischen Kugel :sparkles: eine Frage...", inline=True)
        embed.add_field(name="</minispiel tictactoe:1295784185717592104>",
                        value="> Spiele eine Runde TicTacToe, vielleicht gegen den Bot?", inline=True)
        embed.add_field(name="</afk:1296448860671180882>",
                        value="> Was? Du gehst? | Stelle dich AFK mit einem Grund und benachrichtige Nutzer, wenn sie dich pingen.",
                        inline=False)
        embed.add_field(name="</minecraft skin:1296201414803980290>",
                        value="> Zeige den Minecraft-Skin von einem Nutzer an (Minecraft-Nutzername benötigt).",
                        inline=True)
        embed.add_field(name="</daily:1023319974753878047>",
                        value="> Hol dir deine täglichen <:codingkeks_cookie:1296197308643414027> Kekse von <@1005119817294041209> ab.", inline=True)
        embed.add_field(name="</bake:1202970258822930506>", value="> Backe ein paar leckere <:codingkeks_cookie:1296197308643414027> Kekse.",
                        inline=False)
        embed.set_image(url="https://i.imgur.com/jnoPLVF.png")
        
        await ctx.respond("Bitte warten..", ephemeral=True)
        await ctx.send(embed=embed, view=self.KeksKnopf())

def setup(bot):
    bot.add_cog(CommandsChannel(bot))


