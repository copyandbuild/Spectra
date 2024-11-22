import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Abmeldung(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description="Melde dich ab.")
    @commands.has_role(1300983862222131210)
    async def abmelden(self, ctx: discord.ApplicationContext,
                       zeitraum: Option(str, description="» Der Zeitraum, in dem du nicht erreichbar bist.", required=True),
                       grund: Option(str, description="» Warum meldest du dich ab? Falls es privat ist, schreibe 'Private Gründe'.", required=True)):
        abmeldung_kanal = self.bot.get_channel(1301003782859001957)

        embed = discord.Embed(
            title=f"{ctx.author.display_name} × Abmeldung",
            description=f"**Name**: `{ctx.author.display_name}`\n**Rolle**: {ctx.author.roles[-1].mention}\n**Zeitraum**: `{zeitraum}`\n**Grund**: `{grund}`",
            color=discord.Color.red()
        )

        await abmeldung_kanal.send(embed=embed)

        succem = discord.Embed(
            title="Abmeldung eingereicht",
            description="Deine Abmeldung wurde erfolgreich eingreicht, ein Admin wird sie in kürze anschauen ⌛",
            color=discord.Color.green()
        )
        
        await ctx.respond(embed=succem, ephemeral=True, delete_after=5)

def setup(bot: commands.Bot):
    bot.add_cog(Abmeldung(bot))
