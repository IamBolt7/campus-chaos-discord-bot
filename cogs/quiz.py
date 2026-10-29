import random

import discord
from discord.ext import commands

from utils.quiz_questions import QUIZ_QUESTIONS


class QuizButton(discord.ui.Button):
    def __init__(self, label, correct_answer):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.primary
        )

        self.correct_answer = correct_answer

    async def callback(self, interaction: discord.Interaction):

        view = self.view

        # Only the person who started the quiz can answer
        if interaction.user.id != view.player.id:
            await interaction.response.send_message(
                "💀 Start your own quiz with `/quiz`.",
                ephemeral=True
            )
            return

        # Prevent multiple answers
        if view.answered:
            await interaction.response.send_message(
                "You already answered this question!",
                ephemeral=True
            )
            return

        view.answered = True

        # Disable all buttons
        for item in view.children:
            item.disabled = True

        if self.label == self.correct_answer:

            self.style = discord.ButtonStyle.success

            view.score += 10

            result = (
                f"✅ **Correct!**\n\n"
                f"🔥 +10 points\n"
                f"🏆 Score: **{view.score}**"
            )

        else:

            self.style = discord.ButtonStyle.danger

            # Highlight the correct button
            for item in view.children:
                if item.label == self.correct_answer:
                    item.style = discord.ButtonStyle.success

            result = (
                f"❌ **Wrong!**\n\n"
                f"Correct answer: **{self.correct_answer}**\n"
                f"🏆 Score: **{view.score}**"
            )

        await interaction.response.edit_message(view=view)

        await interaction.followup.send(
            result,
            ephemeral=True
        )


class QuizView(discord.ui.View):
    def __init__(self, player, question):
        super().__init__(timeout=30)

        self.player = player
        self.question = question
        self.score = 0
        self.answered = False

        options = question["options"].copy()
        random.shuffle(options)

        for option in options:
            self.add_item(
                QuizButton(
                    option,
                    question["answer"]
                )
            )

    async def on_timeout(self):

        if self.answered:
            return

        self.answered = True

        for item in self.children:
            item.disabled = True


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="quiz",
        description="Test your knowledge with Campus Chaos 🧠"
    )
    @discord.app_commands.describe(
        category="Choose your quiz category"
    )
    @discord.app_commands.choices(
        category=[
            discord.app_commands.Choice(
                name="💻 Computer Science",
                value="computer_science"
            ),
            discord.app_commands.Choice(
                name="🌍 General Knowledge",
                value="general"
            ),
            discord.app_commands.Choice(
                name="💀 Chaos Mode",
                value="chaos"
            )
        ]
    )
    async def quiz(
        self,
        interaction: discord.Interaction,
        category: discord.app_commands.Choice[str]
    ):

        questions = QUIZ_QUESTIONS[category.value]

        question = random.choice(questions)

        embed = discord.Embed(
            title="🧠 Campus Chaos Quiz",
            description=question["question"],
            color=discord.Color.purple()
        )

        embed.add_field(
            name="Category",
            value=category.name,
            inline=True
        )

        embed.add_field(
            name="Reward",
            value="🔥 10 points",
            inline=True
        )

        embed.set_footer(
            text="You have 30 seconds • Choose wisely"
        )

        view = QuizView(
            interaction.user,
            question
        )

        await interaction.response.send_message(
            embed=embed,
            view=view
        )


async def setup(bot):
    await bot.add_cog(Quiz(bot))