
import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
from database.db import create_tables


# ==========================================================
# ENVIRONMENT CONFIGURATION
# ==========================================================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError(
        "❌ DISCORD_TOKEN not found!\n"
        "Make sure your .env file contains DISCORD_TOKEN."
    )


# ==========================================================
# BOT CONFIGURATION
# ==========================================================

intents = discord.Intents.default()


class CampusChaos(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):

        print("\n🚀 Starting Campus Chaos...\n")

        # Initialize database
        create_tables()
        print("✅ Database initialized!")

        # Load all available Cogs
        extensions = [
            ("cogs.memes", "😂 Meme System"),
            ("cogs.quiz", "🧠 Quiz System"),
            ("cogs.attendance", "📚 Attendance System"),
            ("cogs.fun", "🎲 Fun Commands")
        ]

        for extension, label in extensions:
            try:
                await self.load_extension(extension)
                print(f"✅ {label} loaded!")

            except Exception as error:
                print(f"❌ Failed to load {extension}: {error}")
                raise

        # Sync slash commands once at startup
        try:
            synced = await self.tree.sync()
            print(
                f"\n✅ Synced {len(synced)} global slash commands!"
            )

        except Exception as error:
            print(f"❌ Slash command sync failed: {error}")
            raise


bot = CampusChaos()


# ==========================================================
# BOT READY EVENT
# ==========================================================

@bot.event
async def on_ready():

    print("\n" + "=" * 50)
    print("🎮 CAMPUS CHAOS IS ONLINE!")
    print("=" * 50)

    print(f"🤖 Bot Name: {bot.user}")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"🌐 Connected Servers: {len(bot.guilds)}")
    print(f"📡 Latency: {round(bot.latency * 1000)}ms")

    print("=" * 50)
    print("😈 Let the chaos begin!")
    print("=" * 50 + "\n")


# ==========================================================
# /ping
# ==========================================================

@bot.tree.command(
    name="ping",
    description="Check if Campus Chaos is alive!"
)
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🏓 Pong!",
        description="Campus Chaos is alive and causing trouble.",
        color=discord.Color.green()
    )

    embed.add_field(
        name="📡 Bot Latency",
        value=f"`{latency}ms`",
        inline=True
    )

    embed.add_field(
        name="🟢 Status",
        value="Online",
        inline=True
    )

    embed.set_footer(
        text="Campus Chaos • Powered by questionable decisions"
    )

    await interaction.response.send_message(embed=embed)


# ==========================================================
# /about
# ==========================================================

@bot.tree.command(
    name="about",
    description="Learn about Campus Chaos"
)
async def about(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎮 CAMPUS CHAOS",
        description=(
            "**The Discord bot your college server "
            "definitely didn't need.**\n\n"
            "Built for memes, quizzes, questionable "
            "decisions, and surviving college."
        ),
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="😂 Memes",
        value="Fresh memes for your daily dose of chaos.",
        inline=False
    )

    embed.add_field(
        name="🧠 Quizzes",
        value="Challenge yourself with random trivia.",
        inline=False
    )

    embed.add_field(
        name="📚 Attendance Tracker",
        value="Track your subjects and attendance percentages.",
        inline=False
    )

    embed.add_field(
        name="😈 Bunk Calculator",
        value="Calculate how many classes you can safely miss.",
        inline=False
    )

    embed.add_field(
        name="🎲 Fun Commands",
        value=(
            "Coin flips, dice rolls, roasts, "
            "rizz and random decisions."
        ),
        inline=False
    )

    embed.add_field(
        name="🚧 Coming Soon",
        value="XP, leaderboards, achievements and music.",
        inline=False
    )

    embed.set_footer(
        text="Campus Chaos • Built for fun, not productivity"
    )

    await interaction.response.send_message(embed=embed)


# ==========================================================
# /help
# ==========================================================

@bot.tree.command(
    name="help",
    description="View all Campus Chaos commands"
)
async def help_command(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🎮 CAMPUS CHAOS COMMAND CENTER",
        description=(
            "Welcome to Campus Chaos!\n"
            "Here's everything I can currently do."
        ),
        color=discord.Color.purple()
    )

    # GENERAL COMMANDS
    embed.add_field(
        name="⚙️ GENERAL",
        value=(
            "`/ping` — Check bot latency\n"
            "`/about` — About Campus Chaos\n"
            "`/help` — Show command menu"
        ),
        inline=False
    )

    # MEMES
    embed.add_field(
        name="😂 MEMES",
        value=(
            "`/meme` — Get a random meme"
        ),
        inline=False
    )

    # QUIZ
    embed.add_field(
        name="🧠 QUIZ",
        value=(
            "`/quiz` — Play a trivia quiz"
        ),
        inline=False
    )

    # ATTENDANCE
    embed.add_field(
        name="📚 ATTENDANCE TRACKER",
        value=(
            "`/subject` — Add a subject\n"
            "`/attendance` — View attendance\n"
            "`/attend` — Mark a class attended\n"
            "`/bunk` — Mark a class bunked\n"
            "`/canibunk` — Calculate safe bunks"
        ),
        inline=False
    )

    # FUN COMMANDS
    embed.add_field(
        name="🎲 FUN COMMANDS",
        value=(
            "`/coinflip` — Flip a coin\n"
            "`/roll` — Roll a dice\n"
            "`/8ball` — Ask the Magic 8-Ball\n"
            "`/roast` — Playfully roast a friend\n"
            "`/rizz` — Generate a pickup line\n"
            "`/choose` — Make a random decision"
        ),
        inline=False
    )

    # UPCOMING FEATURES
    embed.add_field(
        name="🚧 COMING SOON",
        value=(
            "🏆 XP & Leaderboards\n"
            "🎖️ Achievements\n"
            "🎵 Music Player"
        ),
        inline=False
    )

    embed.set_footer(
        text="Campus Chaos v1.1 • Let the chaos begin!"
    )

    await interaction.response.send_message(embed=embed)


# ==========================================================
# START CAMPUS CHAOS
# ==========================================================

if __name__ == "__main__":

    print("🎮 Launching Campus Chaos...")

    try:
        bot.run(TOKEN)

    except KeyboardInterrupt:
        print("\n👋 Campus Chaos shutting down...")

    except discord.LoginFailure:
        print("❌ Invalid Discord token. Check your .env file.")
