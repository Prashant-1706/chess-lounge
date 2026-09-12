import os
from dataclasses import dataclass
from urllib.parse import urlencode

import chess
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@dataclass
class Challenge:
    challenger_id: int
    challenged_id: int


@dataclass
class Game:
    white_id: int
    black_id: int
    board: chess.Board
    last_move_uci: str | None = None


challenges: dict[int, Challenge] = {}
games: dict[int, Game] = {}


def board_text(board: chess.Board) -> str:
    rows = []
    for rank in range(7, -1, -1):
        pieces = []
        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            pieces.append(piece.unicode_symbol() if piece else "·")
        rows.append(f"{rank + 1}  " + " ".join(pieces))
    return "```\n" + "\n".join(rows) + "\n\n   a b c d e f g h\n```"


def board_image_url(board: chess.Board, last_move_uci: str | None = None) -> str:
    params: list[tuple[str, str | int]] = [
        ("fen", board.fen()),
        ("size", 700),
        ("orientation", "white"),
        ("light", "EEEED2"),
        ("dark", "769656"),
    ]
    if last_move_uci and len(last_move_uci) >= 4:
        from_square = last_move_uci[:2]
        to_square = last_move_uci[2:4]
        params.extend(
            [
                ("arrows", f"{from_square},{to_square},C8973A"),
                ("highlights", f"{from_square},C8973A"),
                ("highlights", f"{to_square},C8973A"),
            ]
        )
    return "https://deepchess.dev/api/board-image?" + urlencode(params)


def game_embed(game: Game, title: str = "Chess game") -> discord.Embed:
    board = game.board
    turn_id = game.white_id if board.turn == chess.WHITE else game.black_id
    if board.is_game_over():
        outcome = board.outcome()
        status = f"Game over — **{outcome.result()}** ({outcome.termination.name.replace('_', ' ').title()})"
    else:
        status = f"Turn: <@{turn_id}>"
        if board.is_check():
            status += " — **Check!**"
    embed = discord.Embed(title=title, color=discord.Color.green())
    embed.set_image(url=board_image_url(board, game.last_move_uci))
    embed.add_field(name="White", value=f"<@{game.white_id}>")
    embed.add_field(name="Black", value=f"<@{game.black_id}>")
    embed.add_field(name="Status", value=status, inline=False)
    embed.set_footer(text=f"FEN: {board.fen()}")
    return embed


@bot.event
async def on_ready():
    if GUILD_ID:
        guild = discord.Object(id=int(GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    else:
        await bot.tree.sync()
    print(f"Ready as {bot.user}")


@bot.tree.command(description="Create the recommended chess server roles and channels")
@app_commands.checks.has_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("Run this inside a server.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)

    role_specs = [
        ("♔ Grandmaster", discord.Color.gold()),
        ("♕ Tournament Player", discord.Color.blue()),
        ("♙ Chess Member", discord.Color.green()),
    ]
    for name, color in role_specs:
        if not discord.utils.get(guild.roles, name=name):
            await guild.create_role(name=name, color=color, reason="Chess server setup")

    structure = {
        "📌 START HERE": ["welcome", "rules", "announcements", "roles"],
        "♟ CHESS CLUB": ["general-chess", "find-a-game", "chess-games", "puzzles", "opening-lab"],
        "🏆 EVENTS": ["tournaments", "leaderboard", "game-analysis"],
        "🔊 VOICE": ["Casual Games", "Tournament Room", "Study Room"],
        "🛡 STAFF": ["staff-chat", "mod-logs"],
    }
    for category_name, channel_names in structure.items():
        category = discord.utils.get(guild.categories, name=category_name)
        if category is None:
            category = await guild.create_category(category_name, reason="Chess server setup")
        for channel_name in channel_names:
            if discord.utils.get(category.channels, name=channel_name):
                continue
            if category_name == "🔊 VOICE":
                await guild.create_voice_channel(channel_name, category=category)
            else:
                await guild.create_text_channel(channel_name, category=category)

    await interaction.followup.send("Chess server setup complete. Roles and channels are ready!", ephemeral=True)


@bot.tree.command(description="Challenge another member to a chess game")
async def challenge(interaction: discord.Interaction, player: discord.Member):
    if interaction.channel_id in games:
        await interaction.response.send_message("A game is already running in this channel.", ephemeral=True)
        return
    if player.bot or player.id == interaction.user.id:
        await interaction.response.send_message("Choose another human player.", ephemeral=True)
        return
    challenges[interaction.channel_id] = Challenge(interaction.user.id, player.id)
    await interaction.response.send_message(
        f"♟️ {player.mention}, {interaction.user.mention} challenged you! Use `/accept` to play."
    )


@bot.tree.command(description="Accept the pending chess challenge in this channel")
async def accept(interaction: discord.Interaction):
    pending = challenges.get(interaction.channel_id)
    if pending is None or pending.challenged_id != interaction.user.id:
        await interaction.response.send_message("You do not have a pending challenge here.", ephemeral=True)
        return
    game = Game(pending.challenger_id, pending.challenged_id, chess.Board())
    games[interaction.channel_id] = game
    del challenges[interaction.channel_id]
    await interaction.response.send_message(embed=game_embed(game, "Game started!"))


@bot.tree.command(description="Play a move, for example e2e4 or Nf3")
async def move(interaction: discord.Interaction, move: str):
    game = games.get(interaction.channel_id)
    if game is None:
        await interaction.response.send_message("There is no game in this channel.", ephemeral=True)
        return
    expected = game.white_id if game.board.turn == chess.WHITE else game.black_id
    if interaction.user.id != expected:
        await interaction.response.send_message("It is not your turn.", ephemeral=True)
        return
    try:
        try:
            parsed = game.board.parse_san(move.strip())
        except ValueError:
            parsed = chess.Move.from_uci(move.strip().lower())
            if parsed not in game.board.legal_moves:
                raise ValueError
        game.board.push(parsed)
        game.last_move_uci = parsed.uci()
    except ValueError:
        await interaction.response.send_message("That move is not legal. Try `e2e4`, `Nf3`, or `/board`.", ephemeral=True)
        return
    await interaction.response.send_message(embed=game_embed(game, f"Move played: {move}"))
    if game.board.is_game_over():
        del games[interaction.channel_id]


@bot.tree.command(description="Show the current chess board")
async def board(interaction: discord.Interaction):
    game = games.get(interaction.channel_id)
    if game is None:
        await interaction.response.send_message("There is no game in this channel.", ephemeral=True)
        return
    await interaction.response.send_message(embed=game_embed(game))


@bot.tree.command(description="Show information about the current game")
async def game(interaction: discord.Interaction):
    current = games.get(interaction.channel_id)
    if current is None:
        await interaction.response.send_message("There is no game in this channel.", ephemeral=True)
        return
    await interaction.response.send_message(embed=game_embed(current))


@bot.tree.command(description="Resign the current chess game")
async def resign(interaction: discord.Interaction):
    current = games.get(interaction.channel_id)
    if current is None or interaction.user.id not in (current.white_id, current.black_id):
        await interaction.response.send_message("You are not playing a game here.", ephemeral=True)
        return
    winner = current.black_id if interaction.user.id == current.white_id else current.white_id
    del games[interaction.channel_id]
    await interaction.response.send_message(f"🏳️ {interaction.user.mention} resigned. <@{winner}> wins!")


@setup.error
async def setup_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Only a server administrator can run `/setup`.", ephemeral=True)
        return
    raise error


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Copy .env.example to .env and add your token.")

bot.run(TOKEN)
