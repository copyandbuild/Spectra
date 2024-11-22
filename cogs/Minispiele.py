import discord
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup, Option, option
import random
import asyncio
import sqlite3
import json

conn = sqlite3.connect('db/tictactoe.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS games
             (message_id INTEGER PRIMARY KEY, game_state TEXT)''')
conn.commit()

class GameState:
    def __init__(self, player1_id, player2_id, current_player_id, board, game_over, channel_id):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.current_player_id = current_player_id
        self.board = board
        self.game_over = game_over
        self.channel_id = channel_id

    def to_dict(self):
        return {
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'current_player_id': self.current_player_id,
            'board': self.board,
            'game_over': self.game_over,
            'channel_id': self.channel_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['player1_id'],
            data['player2_id'],
            data['current_player_id'],
            data['board'],
            data['game_over'],
            data['channel_id']
        )

class TicTacToe(discord.ui.View):
    def __init__(self, player1, player2, state=None):
        super().__init__(timeout=None)
        self.player1 = player1
        self.player2 = player2
        if state:
            self.current_player = player1 if state.current_player_id == player1.id else player2
            self.board = state.board
            self.game_over = state.game_over
        else:
            self.current_player = player1
            self.board = ["-" for _ in range(9)]
            self.game_over = False

        for i in range(9):
            button = discord.ui.Button(label=self.board[i] if self.board[i] != "-" else "\u200b",
                                       style=discord.ButtonStyle.secondary if self.board[i] == "-" else
                                       (discord.ButtonStyle.primary if self.board[
                                                                           i] == "❌" else discord.ButtonStyle.danger),
                                       row=i // 3, disabled=self.board[i] != "-" or self.game_over)
            button.callback = self.make_move
            self.add_item(button)

    async def make_move(self, interaction: discord.Interaction):
        button = interaction.data["custom_id"]
        index = next(i for i, item in enumerate(self.children) if item.custom_id == button)
        await self.process_move(self.children[index], interaction, index)

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]  
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "-":
                return True
        return False

    def is_board_full(self):
        return "-" not in self.board

    def create_embed(self, title):
        embed = discord.Embed(title="Tic Tac Toe", description=title, color=0x00ff00)
        embed.add_field(name="Spieler 1", value=f"{self.player1.mention} (❌)", inline=True)
        embed.add_field(name="Spieler 2", value=f"{self.player2.mention} (⭕)", inline=True)
        return embed

    def get_winning_move(self, player):
        for i in range(9):
            if self.board[i] == "-":
                self.board[i] = player
                if self.check_winner():
                    self.board[i] = "-"
                    return i
                self.board[i] = "-"
        return None

    def get_best_move(self):
        winning_move = self.get_winning_move("⭕")
        if winning_move is not None:
            return winning_move

        blocking_move = self.get_winning_move("❌")
        if blocking_move is not None:
            return blocking_move

        if self.board[4] == "-":
            return 4

        corners = [0, 2, 6, 8]
        empty_corners = [corner for corner in corners if self.board[corner] == "-"]
        if empty_corners:
            return random.choice(empty_corners)

        empty_cells = [i for i, cell in enumerate(self.board) if cell == "-"]
        return random.choice(empty_cells)

    async def bot_move(self):
        move = self.get_best_move()
        self.board[move] = "⭕"
        self.children[move].label = "⭕"
        self.children[move].style = discord.ButtonStyle.danger
        self.children[move].disabled = True

        if self.check_winner():
            embed = self.create_embed("Der Bot hat gewonnen!")
            await self.message.edit(embed=embed, view=self)
            await self.message.reply(f"{sel} hat gewonnen")
            self.game_over = True
            for child in self.children:
                child.disabled = True
            await self.delete_game_state(self.message.id)
        elif self.is_board_full():
            embed = self.create_embed("Unentschieden!")
            await self.message.reply("Der bot hat gewonnen")
            await self.message.edit(embed=embed, view=self)
            self.game_over = True
            for child in self.children:
                child.disabled = True
            await self.delete_game_state(self.message.id)
        else:
            self.current_player = self.player1
            embed = self.create_embed(f"{self.current_player.mention} ist am Zug.")
            await self.message.edit(embed=embed, view=self)
            await self.save_game_state(self.message.id)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user not in [self.player1, self.player2]:
            await interaction.response.send_message("Du bist nicht Teil dieses Spiels.", ephemeral=True)
            return False
        return True

    async def process_move(self, button, interaction, position):
        if interaction.user != self.current_player:
            await interaction.response.send_message("Du bist nicht am Zug.", ephemeral=True)
            return
        if self.game_over:
            await interaction.response.send_message("Das Spiel ist bereits beendet.", ephemeral=True)
            return

        if self.board[position] == "-":
            symbol = "❌" if self.current_player == self.player1 else "⭕"
            self.board[position] = symbol
            button.label = symbol
            button.style = discord.ButtonStyle.primary if symbol == "❌" else discord.ButtonStyle.danger
            button.disabled = True

            if self.check_winner():
                embed = self.create_embed(f"{self.current_player.mention} hat gewonnen!")
                await self.message.reply(f"{self.current_player.mention} hat gewonnen")
                self.game_over = True
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(embed=embed, view=self)
                await self.delete_game_state(self.message.id)
            elif self.is_board_full():
                embed = self.create_embed("Unentschieden!")
                await self.message.reply(f"{self.current_player.mention} hat gewonnen")
                self.game_over = True
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(embed=embed, view=self)
                await self.delete_game_state(self.message.id)
            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                embed = self.create_embed(f"{self.current_player.mention} ist am Zug.")
                await interaction.response.edit_message(embed=embed, view=self)
                await self.save_game_state(self.message.id)

            if not self.game_over and self.player2.bot and self.current_player == self.player2:
                await self.bot_move()

    async def save_game_state(self, message_id):
        state = GameState(
            self.player1.id,
            self.player2.id,
            self.current_player.id,
            self.board,
            self.game_over,
            self.message.channel.id
        )
        c.execute("""
            INSERT OR REPLACE INTO games (message_id, game_state) 
            VALUES (?, ?)
        """, (message_id, json.dumps(state.to_dict())))
        conn.commit()

    async def delete_game_state(self, message_id):
        c.execute("DELETE FROM games WHERE message_id = ?", (message_id,))
        conn.commit()

class InviteView(discord.ui.View):
    def __init__(self, ctx, opponent):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.opponent = opponent
        self.value = None

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.green)
    async def accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.opponent:
            await interaction.response.defer()
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message("Du kannst diese Einladung nicht annehmen.", ephemeral=True)

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.red)
    async def decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.opponent:
            await interaction.response.defer()
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message("Du kannst diese Einladung nicht ablehnen.", ephemeral=True)

    async def on_timeout(self):
        self.value = False
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.opponent:
            await interaction.response.send_message("Du bist nicht der eingeladene Spieler.", ephemeral=True)
            return False
        return True

class MinispielCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    antworten = [
        "Ja, auf jeden Fall.",
        "Es ist sicher.",
        "Ja, definitiv.",
        "Du kannst darauf zählen.",
        "Ich würde nicht darauf wetten.",
        "Meine Quellen sagen, nein.",
        "Frag später nochmal.",
        "Das sieht nicht gut aus.",
        "Darauf kannst du Gift nehmen!",
        "Sehr unwahrscheinlich",
        "Ich glaube nicht.",
        "Computer sagt nein.",
        "Natürlich",
        "Niemals",
        "Wie kommst du auf die idee?",
        "Das ist doch Quatsch.",
    ]
    
    game = SlashCommandGroup(name="minispiel")

    @game.command(name="tictactoe", description="🎮 › Starte ein TicTacToe Spiel.")
    async def tictactoe(self, ctx, opponent: discord.Member = None):
        if opponent is None or opponent.bot:
            opponent = self.bot.user
            game = TicTacToe(ctx.author, opponent)
            embed = game.create_embed(f"{ctx.author.mention} ist am Zug.")
            response = await ctx.respond(embed=embed, view=game)
            game.message = await response.original_response()
            await game.save_game_state(game.message.id)
        else:
            invite_embed = discord.Embed(
                title="Tic Tac Toe Einladung",
                description=f"{ctx.author.mention} fordert {opponent.mention} zu einem Spiel Tic Tac Toe heraus, {opponent.mention} hat 5 Minuten Zeit es anzunehmen! ",
                color=discord.Color.blue()
            )
            invite_view = InviteView(ctx, opponent)
            invite_message = await ctx.respond(embed=invite_embed, view=invite_view)

            await invite_view.wait()

            if invite_view.value is True:
                await asyncio.sleep(2)
                game = TicTacToe(ctx.author, opponent)
                embed = game.create_embed(f"{ctx.author.mention} ist am Zug.")
                game_message = await invite_message.edit(embed=embed, view=game)
                game.message = game_message
                await game.save_game_state(game_message.id)
            elif invite_view.value is False:
                decline_embed = discord.Embed(
                    title="Tic Tac Toe Einladung abgelehnt",
                    description=f"{opponent.mention} hat die Einladung abgelehnt oder die Zeit ist abgelaufen.",
                    color=discord.Color.red()
                )
                await invite_message.edit(embed=decline_embed, view=None)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_games()

    async def load_games(self):
        c.execute("SELECT * FROM games")
        for row in c.fetchall():
            message_id, game_state_json = row
            game_state = GameState.from_dict(json.loads(game_state_json))

            try:
                channel = self.bot.get_channel(game_state.channel_id)
                message = await channel.fetch_message(message_id)
                player1 = await self.bot.fetch_user(game_state.player1_id)
                player2 = await self.bot.fetch_user(game_state.player2_id)

                game = TicTacToe(player1, player2, state=game_state)
                game.message = message
                current_player = player1 if game_state.current_player_id == player1.id else player2

                if game_state.game_over:
                    embed = game.create_embed("Spiel beendet.")
                    await message.edit(embed=embed, view=game)
                    await game.delete_game_state(message_id)
                else:
                    embed = game.create_embed(f"{current_player.mention} ist am Zug.")
                    await message.edit(embed=embed, view=game)
            except discord.errors.NotFound:
                c.execute("DELETE FROM games WHERE message_id = ?", (message_id,))
                conn.commit()

########################### 8BALL GAME ####################################
    @game.command(name='8ball')
    async def eight_ball(self, ctx, frage: Option(str, "Welche frage möchtest du der Magischen Kugel stellen?", required=True)):
        response = random.choice(self.antworten)

        embed = discord.Embed(
            title="Blocktopia × 🎱",
            description=f"{ctx.author.mention} sich die frage: {frage}...\nDie Magische Kugel denkt nach..",
            color=discord.Colour.blue()
        )
        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar.url}")

        message = await ctx.respond(embed=embed)
        await asyncio.sleep(2)
        newembed = discord.Embed(
            title="Blocktopia × 🎱",
            description=f"{ctx.author.mention} sich die frage: {frage}...\nDie Magische Kugel sagt: `{response}`",
            color=discord.Colour.blue()
        )
        newembed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar.url}")
        await message.edit(embed=newembed)
########################### 8BALL GAME ####################################

    @game.command(name='würfel')
    async def roll_dice(self, ctx, bis: Option(int, "Bis zu welcher Zahl soll der Würfel würfeln können?", required=False, default=6),
                        unsichtbar: Option(bool, "Soll die nachricht nur für dich sichtbar sein?", required=False, default=False)):
        response = random.randint(1, bis)

        embed = discord.Embed(
            title="Blocktopia × 🎲",
            description=f"{ctx.author.mention} würfelt die Zahl **{response}**",
            color=discord.Color.blue()
        )

        embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar.url}")
        await ctx.respond(embed=embed, ephemeral=unsichtbar)

def setup(bot):
    bot.add_cog(MinispielCog(bot))
