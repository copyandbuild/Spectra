import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
from discord.utils import get

class TeamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manage_role = 1309257445704601710
        self.team_role = 1300983862222131210

    team = SlashCommandGroup("team")

    async def notify_user(self, user, message):
        try:
            await user.send(message)
        except Exception:
            return False
        return True

    async def log_action(self, action, user_name, role_name=None, grund=None):
        log_channel = await self.bot.fetch_channel(1309257580006346865)
        if grund:
            await log_channel.send(f"{action} | {user_name}\n> **Grund: {grund}**")
        elif role_name:
            await log_channel.send(f"{action} | {user_name}\n> **{role_name}**")
        else:
            await log_channel.send(f"{action} | {user_name}")

    @team.command(description="Füge jemanden ins Team hinzu")
    async def hinzufügen(
        self,
        ctx,
        nutzer: Option(discord.Member, "Wähle den Nutzer, den du ins Team hinzufügen möchtest", required=True),
        rolle: Option(discord.Role, "Wähle die Rolle aus, die du ihm direkt geben möchtest", required=False)
    ):

        roles = {
            "Admin": 1300983860254871565,
            "Moderator": 1300983861177614367
        }

        if not get(ctx.author.roles, id=self.manage_role):
            await ctx.respond("Du benötigst die <@&1305988293422485584> Rolle, um dies zu tun.", ephemeral=True)
            return

        if rolle.id not in roles:
            await ctx.respond("Diese Rolle ist nicht für ein Teammitglied erreichbar.", ephemeral=True)
            return

        default_role_id = 1304691036047802369
        role = rolle or get(ctx.guild.roles, id=default_role_id)
        await nutzer.add_roles(role, reason=f"/team hinzufügen Command - {ctx.author.display_name}")
        await nutzer.add_roles(self.team_role, reason=f"/team hinzufügen Command - {ctx.author.display_name}")
        await self.log_action("[+] Hinzugefügt", nutzer.display_name, role.name)
        await ctx.respond(f"{nutzer.mention} wurde dem Team als **{role.name}** hinzugefügt.", ephemeral=True)

    @team.command(description="Hochstufen eines Teammitglieds")
    async def hochstufen(
        self,
        ctx,
        nutzer: Option(discord.Member, "Wähle das Teammitglied, das hochgestuft werden soll", required=True)
    ):
        if not get(ctx.author.roles, id=self.manage_role):
            await ctx.respond("Du benötigst die <@&1305988293422485584> Rolle, um dies zu tun.", ephemeral=True)
            return

        roles = {
            "Admin": 1300983860254871565,
            "Moderator": 1300983861177614367
        }

        current_role = None
        for role_name, role_id in roles.items():
            if get(ctx.guild.roles, id=role_id) in nutzer.roles:
                current_role = role_name
                break

        if not current_role:
            await ctx.respond(f"{nutzer.mention} hat keine Teamrolle, die hochgestuft werden kann.", ephemeral=True)
            return

        next_role = None
        if current_role == "Supporter":
            next_role = "Moderator"
        elif current_role == "Moderator":
            next_role = "Admin"
        else:
            await ctx.respond(f"{nutzer.mention} ist bereits Admin.", ephemeral=True)
            return

        next_role_id = roles[next_role]
        next_role_obj = get(ctx.guild.roles, id=next_role_id)
        await nutzer.add_roles(next_role_obj, reason=f"/team hochstufen Command - {ctx.author.display_name}")
        next_role_obj.name = next_role_obj.name[2:]
        await self.log_action("[+] Hochgestuft", nutzer.display_name, next_role_obj.name)
        await ctx.respond(f"{nutzer.mention} wurde hochgestuft zu **{next_role_obj.name}**", ephemeral=True)

    @team.command(description="Runterstufen eines Teammitglieds")
    async def runterstufen(
        self,
        ctx,
        nutzer: Option(discord.Member, "Wähle das Teammitglied, das runtergestuft werden soll", required=True)
    ):
        if not get(ctx.author.roles, id=1305988293422485584):
            await ctx.respond("Du benötigst die <@&1305988293422485584> Rolle, um dies zu tun.", ephemeral=True)
            return

        roles = {
            "Admin": 1300983860254871565,
            "Moderator": 1300983861177614367
        }

        current_role = None
        for role_name, role_id in roles.items():
            if get(ctx.guild.roles, id=role_id) in nutzer.roles:
                current_role = role_name
                break

        if not current_role:
            await ctx.respond(f"{nutzer.mention} hat keine Teamrolle, die runtergestuft werden kann.", ephemeral=True)
            return

        next_role = None
        if current_role == "Admin":
            next_role = "Moderator"
        elif current_role == "Moderator":
            next_role = "Supporter"
        else:
            await ctx.respond(f"{nutzer.mention} ist bereits Supporter.", ephemeral=True)
            return

        next_role_id = roles[next_role]
        next_role_obj = get(ctx.guild.roles, id=next_role_id)
        await nutzer.add_roles(next_role_obj, reason=f"/team runterstufen Command - {ctx.author.display_name}")
        await nutzer.remove_roles(get(ctx.guild.roles, id=roles[current_role]), reason=f"/team runterstufen Command - {ctx.author.display_name}")
        next_role_obj.name = next_role_obj.name[2:]
        await self.log_action("[-] Runtergestuft", nutzer.display_name, next_role_obj.name)
        await ctx.respond(f"{nutzer.mention} wurde runtergestuft zu **{next_role_obj.name}**", ephemeral=True)

    @team.command(description="Verwarne ein Teammitglied")
    async def warnen(
        self,
        ctx,
        nutzer: Option(discord.Member, "Wähle das Teammitglied, das verwarnt werden soll", required=True),
        grund: Option(str, "Gib den Grund für die Verwarnung an", required=True)
    ):
        if not get(ctx.author.roles, id=1305988293422485584):
            await ctx.respond("Du benötigst die <@&1305988293422485584> Rolle, um dies zu tun.", ephemeral=True)
            return

        warn_roles = [
            get(ctx.guild.roles, id=1309257801918447637),
            get(ctx.guild.roles, id=1309257807689941042),
            get(ctx.guild.roles, id=1309257811087331438),
        ]

        current_warning_level = sum(1 for role in warn_roles if role in nutzer.roles)

        if current_warning_level < 3:
            next_warn_role = warn_roles[current_warning_level]
            await nutzer.add_roles(next_warn_role, reason=f"Verwarnung durch {ctx.author.display_name}: {grund}")
            await self.log_action(f"[!] Verwarnung (Warnstufe {current_warning_level + 1})", nutzer.display_name, grund=grund)
            await ctx.respond(f"{nutzer.mention} hat nun **{current_warning_level + 1} Team-Warnung(en)**. Grund: **{grund}**", ephemeral=True)
            await self.notify_user(nutzer, f"**ACHTUNG**! Du wurdest wegen dem Grund `{grund}` verwarnt! Warnungsstufe: {current_warning_level + 1}. Beachte: Bei 3 Verwarnungen wirst du aus dem Team entfernt.")
        else:
            for warn_role in warn_roles:
                await nutzer.remove_roles(warn_role, reason="Automatische Entfernung nach 3. Warnung")
            await self.entfernen(ctx, nutzer)
            await ctx.respond(f"{nutzer.mention} wurde nach der 3. Warnung aus dem Team entfernt.", ephemeral=True)

    @team.command(description="Entferne ein Teammitglied")
    async def entfernen(
        self,
        ctx,
        nutzer: discord.Member,
    ):
        member_role_id = 1304691036047802369
        admin_role_id = 1304689028175630428

        roles_to_remove = [get(ctx.guild.roles, id=admin_role_id), get(ctx.guild.roles, id=member_role_id)]
        await nutzer.remove_roles(*roles_to_remove, reason=f"/team entfernen Command - {ctx.author.display_name}")
        if not await self.notify_user(nutzer, "Du wurdest aus dem LarroxUnity-Team entfernt."):
            await ctx.respond("Ich konnte dem Nutzer keine Nachricht senden. Stelle sicher, dass DMs aktiviert sind.", ephemeral=True)
        await self.log_action("[-] Entfernt", nutzer.display_name)
        await ctx.respond(f"{nutzer.mention} wurde erfolgreich aus dem Team entfernt.", ephemeral=True)

def setup(bot):
    bot.add_cog(TeamCog(bot))
