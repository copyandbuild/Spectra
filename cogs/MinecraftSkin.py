import discord
from discord.ext import commands
import asyncio
from discord import Option, SlashCommandGroup
import aiohttp

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ses = None  # Initialize as None

    async def setup_session(self):
        self.ses = aiohttp.ClientSession()

    minecraft = SlashCommandGroup(name="minecraft", description="🎮 | Hier kannst du dir Informationen über Minecraft Server anzeigen lassen!")

    @minecraft.command(name="skin", description="🎮 | Zeigt dir den Skin eines Minecraft Spielers an!")
    async def skin(self, ctx, name: Option(str, "Der Name des Minecraft Spielers", required=True)):
        if not ctx.channel.permissions_for(ctx.guild.me).send_messages:
            embed = discord.Embed(
                title="**`❌` | Fehler**",
                description="> Ich habe keine Rechte um Nachrichten zu senden!",
                color=0x2B2D31
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        
        async with self.ses.get(f"https://api.mojang.com/users/profiles/minecraft/{name}") as resp:
            if resp.status != 200:
                embed = discord.Embed(
                    title="**`❌` | Fehler**",
                    description="> Der Spieler existiert nicht!",
                    color=0x2B2D31
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return
            
            jj = await resp.json()
            uuid = jj.get("id")
            if uuid is None:
                embed = discord.Embed(
                    title="**`❌` | Fehler**",
                    description="> Der Spieler existiert nicht!",
                    color=0x2B2D31
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return

            skin_url = f"https://mc-heads.net/body/{uuid}/right"
            head_url = f"https://minotar.net/cube/{uuid}/512.png"
            load_embed = discord.Embed(
                title="**`⌛` | Lade...**",
                description="> Skin wird geladen...",
                color=0x2B2D31
            )
            await ctx.respond(embed=load_embed)
            
            await asyncio.sleep(1)  # Simulate loading time
            name_upper = name.upper()
            embed = discord.Embed(
                title=f"`🎮` | SKIN | {name_upper}",
                description=f"> Das ist der Skin von {name}!",
                color=0x2B2D31
            )
            embed.set_image(url=skin_url)
            embed.set_thumbnail(url=head_url)
            await ctx.edit(embeds=[embed])

    async def cog_load(self):
        await self.setup_session()

    def cog_unload(self):
        if self.ses:
            asyncio.create_task(self.ses.close())

def setup(bot):
    bot.add_cog(Minecraft(bot))
    bot.loop.create_task(bot.get_cog("Minecraft").cog_load())
