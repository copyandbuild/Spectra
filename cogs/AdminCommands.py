import discord
from discord.ext import commands
from discord.commands import slash_command, Option, SlashCommandGroup

class AdminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    admin = SlashCommandGroup("admin", default_member_permissions=discord.Permissions(administrator=True))

    @admin.command(description="Melde dich ab.")
    @commands.has_role(1304691296895631450)
    async def abmelden(self, ctx: discord.ApplicationContext,
                       nutzer: Option(discord.Member, description="» Wen Möchtest du abmelden?"),

                       zeitraum: Option(str, description="» Der Zeitraum, in dem du nicht erreichbar bist.", required=True),
                       grund: Option(str, description="» Warum meldest du dich ab? Falls es privat ist, schreibe 'Private Gründe'.", required=True)):
        abmeldung_kanal = self.bot.get_channel(1284969905460088893)

        embed = discord.Embed(
            title=f"{nutzer.display_name} × Abmeldung",
            description=f"**Name**: `{nutzer.display_name}`\n**Rolle**: {nutzer.roles[-1].mention}\n**Zeitraum**: `{zeitraum}`\n**Grund**: `{grund}`",
            color=discord.Color.red()
        )

        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.display_avatar}")

        await abmeldung_kanal.send(embed=embed)

        succem = discord.Embed(
            title="Abmeldung eingereicht",
            description=f"> Du hast erfolgreich {nutzer.mention} Abgemeldet. :white_check_mark:",
            color=discord.Color.green()
        )

        await ctx.respond(embed=succem, ephemeral=True, delete_after=5)

def setup(bot: commands.Bot):
    bot.add_cog(AdminCommands(bot))
