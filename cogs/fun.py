
import random

import discord
from discord import app_commands
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ==========================================
    # 1. COIN FLIP
    # ==========================================

    @app_commands.command(
        name="coinflip",
        description="Flip a coin and test your luck!"
    )
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])

        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"The coin landed on **{result}!**",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(embed=embed)

    # ==========================================
    # 2. DICE ROLL
    # ==========================================

    @app_commands.command(
        name="roll",
        description="Roll a dice with customizable sides"
    )
    @app_commands.describe(sides="Number of sides on the dice")
    async def roll(
        self,
        interaction: discord.Interaction,
        sides: app_commands.Range[int, 2, 1000] = 6
    ):
        result = random.randint(1, sides)

        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=(
                f"Dice: **D{sides}**\n"
                f"You rolled: **{result}**"
            ),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed)

    # ==========================================
    # 3. MAGIC 8-BALL
    # ==========================================

    @app_commands.command(
        name="8ball",
        description="Ask the magical 8-ball a question"
    )
    @app_commands.describe(question="Your yes-or-no question")
    async def eightball(
        self,
        interaction: discord.Interaction,
        question: str
    ):
        if not question.strip():
            await interaction.response.send_message(
                "❌ Ask me a question first!",
                ephemeral=True
            )
            return

        answers = [
            "Absolutely! 😎",
            "Yes, definitely.",
            "Signs point to yes.",
            "Maybe, maybe not. 👀",
            "Ask again after lunch.",
            "Very doubtful.",
            "No chance. 💀",
            "My sources say no.",
            "The universe says yes. ✨",
            "Even Google doesn't know.",
            "Focus on your attendance first. 📚",
            "That's classified information. 🤫"
        ]

        answer = random.choice(answers)

        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="Your Question",
            value=question[:1024],
            inline=False
        )

        embed.add_field(
            name="The Answer",
            value=answer,
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    # ==========================================
    # 4. FRIENDLY ROAST
    # ==========================================

    @app_commands.command(
        name="roast",
        description="Playfully roast a Discord member"
    )
    @app_commands.describe(member="The member to roast")
    async def roast(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        roasts = [
            "Your Wi-Fi has more consistency than your decisions.",
            "You have the energy of a laptop at 2% battery.",
            "Your brain has 47 tabs open and none are responding.",
            "Even your autocorrect has given up on you.",
            "You're the human version of a loading screen.",
            "Your attendance has more plot twists than a Netflix series.",
            "You're not lagging, you're just thinking in slow motion.",
            "Your code has more bugs than a rainforest.",
            "You bring the same energy as a Monday morning lecture.",
            "Your GitHub commits are rarer than college holidays."
        ]

        roast = random.choice(roasts)

        embed = discord.Embed(
            title="🔥 Roast Generator",
            description=f"{member.mention}\n\n**{roast}**",
            color=discord.Color.red()
        )

        embed.set_footer(text="Just jokes! Don't take it seriously.")

        await interaction.response.send_message(embed=embed)

    # ==========================================
    # 5. RIZZ GENERATOR
    # ==========================================

    @app_commands.command(
        name="rizz",
        description="Generate a random pickup line"
    )
    async def rizz(self, interaction: discord.Interaction):
        lines = [
            "Are you Wi-Fi? Because I'm feeling a connection. 📶",
            "Are you Python? Because you make my life easier. 🐍",
            "Are you a keyboard? Because you're just my type. ⌨️",
            "Are you GitHub? Because I want to commit to you. 💻",
            "Are you an API? Because you've got my attention.",
            "Are you a compiler? Because you make my heart race.",
            "Are you a database? Because I can't stop querying you.",
            "Are you a semicolon? Because you complete my statements.",
            "Are you Bluetooth? Because I think we're paired.",
            "Are you a 404 error? Because I can't find anyone like you."
        ]

        line = random.choice(lines)

        embed = discord.Embed(
            title="💘 Rizz Generator",
            description=line,
            color=discord.Color.magenta()
        )

        embed.set_footer(text="Campus Chaos Certified Rizz™")

        await interaction.response.send_message(embed=embed)

    # ==========================================
    # 6. RANDOM CHOICE
    # ==========================================

    @app_commands.command(
        name="choose",
        description="Let Campus Chaos choose between options"
    )
    @app_commands.describe(
        options="Comma-separated options, e.g. pizza, burger, momos"
    )
    async def choose(
        self,
        interaction: discord.Interaction,
        options: str
    ):
        choices = [
            item.strip()
            for item in options.split(",")
            if item.strip()
        ]

        if len(choices) < 2:
            await interaction.response.send_message(
                "❌ Give me at least two options separated by commas!",
                ephemeral=True
            )
            return

        if len(choices) > 20 or any(len(c) > 100 for c in choices):
            await interaction.response.send_message(
                "❌ Use at most 20 options, each under 100 characters.",
                ephemeral=True
            )
            return

        selected = random.choice(choices)

        embed = discord.Embed(
            title="🎯 Decision Maker",
            description=f"I choose...\n\n**{selected}** 🎉",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
