
import random

import discord
from discord import app_commands
from discord.ext import commands

from utils.quiz_questions import QUIZ_QUESTIONS
from utils.xp import add_xp


# ==========================================================
# QUIZ ANSWER BUTTON
# ==========================================================

class QuizButton(discord.ui.Button):

    def __init__(self, label, correct_answer):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.primary
        )

        self.correct_answer = correct_answer

    async def callback(self, interaction: discord.Interaction):

        view = self.view

        # Only the player who started the quiz can answer.
        if interaction.user.id != view.player.id:
            await interaction.response.send_message(
                "💀 Start your own quiz with `/quiz`.",
                ephemeral=True
            )
            return

        # Prevent duplicate answers.
        if view.answered:
            await interaction.response.send_message(
                "⚠️ You already answered this quiz!",
                ephemeral=True
            )
            return

        view.answered = True
        view.stop()

        # Disable all answer buttons.
        for item in view.children:
            item.disabled = True

        if self.label == self.correct_answer:

            self.style = discord.ButtonStyle.success

            # Award XP and record one quiz win.
            xp_result = add_xp(
                interaction.user.id,
                amount=25,
                quiz_win=True
            )

            message = (
                "✅ **CORRECT ANSWER!**\n\n"
                "🔥 **+25 XP**\n"
                f"⭐ Level: **{xp_result['level']}**\n"
                f"🏆 Total XP: **{xp_result['xp']}**\n"
                f"🧠 Quiz Wins: **{xp_result['quiz_wins']}**"
            )

            # Announce newly unlocked achievements.
            if xp_result["unlocked"]:
                message += "\n\n🎖️ **Achievement Unlocked!**\n"
                message += "\n".join(xp_result["unlocked"])

        else:

            self.style = discord.ButtonStyle.danger

            # Highlight the correct answer.
            for item in view.children:
                if item.label == self.correct_answer:
                    item.style = discord.ButtonStyle.success

            message = (
                "❌ **WRONG ANSWER!**\n\n"
                f"✅ Correct answer: **{self.correct_answer}**\n\n"
                "💀 No XP this time. Better luck next round!"
            )

        # Update the original quiz message.
        await interaction.response.edit_message(view=view)

        # Send the result privately to the player.
        await interaction.followup.send(
            message,
            ephemeral=True
        )


# ==========================================================
# QUIZ VIEW
# ==========================================================

class QuizView(discord.ui.View):

    def __init__(self, player, question):
        super().__init__(timeout=30)

        self.player = player
        self.question = question
        self.answered = False
        self.message = None

        options = question["options"].copy()
        random.shuffle(options)

        for option in options:
            self.add_item(
                QuizButton(
                    label=option,
                    correct_answer=question["answer"]
                )
            )

    async def on_timeout(self):

        if self.answered:
            return

        self.answered = True

        for item in self.children:
            item.disabled = True

        # Disable expired buttons in Discord.
        if self.message:
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass


# ==========================================================
# QUIZ COG
# ==========================================================

class Quiz(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="quiz",
        description="Test your knowledge with Campus Chaos 🧠"
    )
    @app_commands.describe(
        category="Choose your quiz category"
    )
    @app_commands.choices(
        category=[
            app_commands.Choice(
                name="💻 Computer Science",
                value="computer_science"
            ),
            app_commands.Choice(
                name="🌍 General Knowledge",
                value="general"
            ),
            app_commands.Choice(
                name="💀 Chaos Mode",
                value="chaos"
            )
        ]
    )
    async def quiz(
        self,
        interaction: discord.Interaction,
        category: app_commands.Choice[str]
    ):

        questions = QUIZ_QUESTIONS.get(category.value, [])

        if not questions:
            await interaction.response.send_message(
                "❌ No questions available for this category.",
                ephemeral=True
            )
            return

        question = random.choice(questions)

        embed = discord.Embed(
            title="🧠 Campus Chaos Quiz",
            description=question["question"],
            color=discord.Color.purple()
        )

        embed.add_field(
            name="📚 Category",
            value=category.name,
            inline=True
        )

        embed.add_field(
            name="🔥 Reward",
            value="25 XP for a correct answer",
            inline=True
        )

        embed.set_footer(
            text="⏱️ 30 seconds • Choose wisely!"
        )

        view = QuizView(
            player=interaction.user,
            question=question
        )

        await interaction.response.send_message(
            embed=embed,
            view=view
        )

        # Save the message so buttons can be
        # disabled when the quiz times out.
        view.message = await interaction.original_response()


# ==========================================================
# LOAD QUIZ COG
# ==========================================================

async def setup(bot):
    await bot.add_cog(Quiz(bot))
