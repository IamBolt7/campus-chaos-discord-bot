import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Make sure the token exists
if not TOKEN:
    raise ValueError(
        "DISCORD_TOKEN was not found. "
        "Make sure you added it to your .env file."
    )

# Discord intents
intents = discord.Intents.default()

# Create bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)
async def setup_hook():
    await bot.load_extension("cogs.memes")
    await bot.load_extension("cogs.quiz")
    
    print("😂 Meme system loaded!")
    print("🧠 Quiz system loaded!")


bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print("=" * 45)
    print(f"🟢 Campus Chaos is ONLINE!")
    print(f"🤖 Logged in as: {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print("=" * 45)

    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as error:
        print(f"❌ Command sync failed: {error}")


# -------------------------
# /ping
# -------------------------

@bot.tree.command(
    name="ping",
    description="Check if Campus Chaos is alive!"
)
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"🏓 **Pong!**\n"
        f"Campus Chaos is alive.\n"
        f"Latency: `{latency}ms`"
    )


# -------------------------
# /about
# -------------------------

@bot.tree.command(
    name="about",
    description="Learn about Campus Chaos"
)
async def about(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎮 Campus Chaos",
        description=(
            "The Discord bot your college server "
            "definitely didn't need."
        ),
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="😂 Fun",
        value="Memes, jokes and random chaos",
        inline=False
    )

    embed.add_field(
        name="🧠 Quiz",
        value="Quizzes, XP and leaderboards",
        inline=False
    )

    embed.add_field(
        name="📚 Bunk Planner",
        value="Track attendance and calculate safe bunks",
        inline=False
    )

    embed.add_field(
        name="🎵 Music",
        value="Coming later!",
        inline=False
    )

    embed.set_footer(
        text="Campus Chaos • Built for fun"
    )

    await interaction.response.send_message(embed=embed)


# -------------------------
# /help
# -------------------------

@bot.tree.command(
    name="help",
    description="Show Campus Chaos commands"
)
async def help_command(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎮 Campus Chaos Commands",
        description="Here's what I can currently do:",
        color=discord.Color.green()
    )

    embed.add_field(
        name="⚙️ General",
        value=(
            "`/ping` — Check bot latency\n"
            "`/about` — About Campus Chaos\n"
            "`/help` — Show this menu"
        ),
        inline=False
    )

    embed.add_field(
        name="😂 Fun",
        value=(
            "`/meme` — Get a random meme"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🧠 Quiz",
        value=(
            "`/quiz` — Play a random quiz"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🚧 Coming Soon",
        value=(
            "📊 Attendance Tracker\n"
            "😈 Bunk Calculator\n"
            "🏆 XP & Leaderboard\n"
            "🎵 Music"
        ),
        inline=False
    )
    

    await interaction.response.send_message(embed=embed)


# Start the bot
bot.run(TOKEN)