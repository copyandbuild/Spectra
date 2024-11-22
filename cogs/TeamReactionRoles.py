import discord
from discord.commands import slash_command
from discord.ext import commands

class ReactionRolesTeam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class ReactionView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Ticket Ping", style=discord.ButtonStyle.green, emoji="🎫", custom_id="ticket-button")
        async def ticket_callback(self, button: discord.Button, interaction: discord.Interaction):
            if not interaction.guild.me.guild_permissions.manage_roles:
                await interaction.response.send_message(
                    "> Ich habe nicht die erforderlichen Berechtigungen, um Rollen zu verwalten.", ephemeral=True)
                return

            role_id = 1295487334569214003
            role = interaction.guild.get_role(role_id)

            if role is None:
                await interaction.response.send_message("Die Rolle konnte nicht gefunden werden.", ephemeral=True)
                return

            if role in interaction.user.roles:
                await interaction.user.remove_roles(role, reason="Ticket Button")
                embed = discord.Embed(
                    title="Blocktopia × Rolle Entfernt",
                    description=f"[-] <@&{role_id}>",
                    color=discord.Color.red()
                )
            else:
                await interaction.user.add_roles(role, reason="Ticket Button")
                embed = discord.Embed(
                    title="Blocktopia × Rolle Hinzugefügt",
                    description=f"[+] <@&{role_id}>",
                    color=discord.Color.green()
                )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        @discord.ui.button(label="Modmail Ping", style=discord.ButtonStyle.green, emoji="📥", custom_id="modmail-button")
        async def modmail_callback(self, button: discord.Button, interaction: discord.Interaction):
            if not interaction.guild.me.guild_permissions.manage_roles:
                await interaction.response.send_message(
                    "Ich habe nicht die erforderlichen Berechtigungen, um Rollen zu verwalten.", ephemeral=True)
                return

            role_id = 1295482202330501241
            role = interaction.guild.get_role(role_id)

            if role is None:
                await interaction.response.send_message("Die Rolle konnte nicht gefunden werden.", ephemeral=True)
                return

            if role in interaction.user.roles:
                await interaction.user.remove_roles(role, reason="Modmail Button")
                embed = discord.Embed(
                    title="Blocktopia × Rolle Entfernt",
                    description=f"[-] <@&{role_id}>",
                    color=discord.Color.red()
                )
            else:
                await interaction.user.add_roles(role, reason="Modmail Button")
                embed = discord.Embed(
                    title="Blocktopia × Rolle Hinzugefügt",
                    description=f"[+] <@&{role_id}>",
                    color=discord.Color.green()
                )

            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(self.ReactionView())

    @slash_command(description="LARROX ONLY COMMAND | Ping Roles")
    async def teampingroles(self, ctx):
        if ctx.author.id != 1143510845368832111:
            await ctx.respond("> Hm, sieht so aus als wärst du nicht <@1143510845368832111>.", ephemeral=True)
            return

        await ctx.respond("sending team ping roles...", ephemeral=True)

        embed = discord.Embed(
            title="Blocktopia × Reaktionsrollen",
            description="`🎫` **Ticket Ping**\n- Werde bei neuen Tickets Erwähnt, um es schneller zu Bearbeiten\n\n`📥` **Modmail Ping**\n- Werde bei einer Neuen Modmail benachrichtigt.\n\n**Ticket sowie Modmail sind nur Channels auf diesem Discord Server!**",
            color=discord.Color.green()
        )

        view = self.ReactionView()
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(ReactionRolesTeam(bot))
