import asyncio

import discord
from discord.ext import commands
import sqlite3

class CountingCog(commands.Cog):
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
        self.conn = sqlite3.connect('db/counting_system.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS counting (
                          guild_id INTEGER PRIMARY KEY,
                          last_number INTEGER,
                          last_user_id INTEGER
                          )''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.id != self.channel_id:
            return
        try:
            number = int(message.content)
            await self.handle_counting(message, number)
        except ValueError:
            return
        except Exception as e:
            print(f"An error occurred: {e}")

    async def handle_counting(self, message, number):
        row = self.c.execute('SELECT last_number, last_user_id FROM counting WHERE guild_id = ?',
                             (message.guild.id,)).fetchone()

        if row:
            last_number, last_user_id = row
            if last_number is None:
                await self.handle_first_counting(message, number)
            elif number == last_number + 1 and last_user_id != message.author.id:
                await self.handle_correct_counting(message, number)
            else:
                await self.handle_incorrect_counting(message, last_user_id)
        else:
            await self.handle_first_counting(message, number)

    async def handle_correct_counting(self, message, number):
        await message.add_reaction('✅')
        guild = await self.bot.fetch_guild(1282103026760417382)
        channel = await guild.fetch_channel(self.channel_id)
        await channel.edit(topic=f"Derzeitige Nummer: {number + 1} (Die schreibst du in den Chat bitti...)")

        self.c.execute('UPDATE counting SET last_number = ?, last_user_id = ? WHERE guild_id = ?',
                       (number, message.author.id, message.guild.id))
        self.conn.commit()
        if number % 100 == 0:
            await message.add_reaction('🔥')
            complete_message = await message.channel.send(f"Herzlichen Glückwunsch! Wir sind jetzt bei der Nummer: ``WIRD GELADEN...`` 🎉. Weiter so!")
            await asyncio.sleep(1)
            await complete_message.edit(f"Herzlichen Glückwunsch! Wir sind jetzt bei der Nummer: ``{number}`` 🎉. Weiter so!")

    async def handle_incorrect_counting(self, message, last_user_id):
        await message.add_reaction('❌')
        row = self.c.execute('SELECT last_number FROM counting WHERE guild_id = ?', (message.guild.id,)).fetchone()
        if row:
            last_number = row[0]
            if last_user_id == message.author.id:
                warning_message = await message.channel.send(
                    f"{message.author.mention} Du kannst nicht zweimal hintereinander zählen!")
                await message.delete(delay=5)
                await warning_message.delete(delay=5)
            else:
                warning_message = await message.channel.send(
                    f"{message.author.mention} Du hast falsch gezählt, die nächste Zahl wäre ``{last_number + 1}``.")
                await message.delete(delay=5)
                await warning_message.delete(delay=5)

    async def handle_first_counting(self, message, number):
        self.c.execute('INSERT OR IGNORE INTO counting (guild_id, last_number, last_user_id) VALUES (?, ?, ?)',
                       (message.guild.id, number, message.author.id))
        self.conn.commit()
        await message.add_reaction('✅')

    def __del__(self):
        self.c.close()
        self.conn.close()


def setup(bot):
    channel_id = 1309257146583613513
    bot.add_cog(CountingCog(bot, channel_id))
