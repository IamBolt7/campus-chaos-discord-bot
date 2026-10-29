
import discord
from discord import app_commands
from discord.ext import commands

from database.db import get_connection
from utils.xp import (
    ACHIEVEMENTS,
    get_profile,
    get_achievements
)


class Levels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ========================================
    # /profile
    # ========================================

    @app_commands.command(
        name="profile",
        description="View your Campus Chaos profile"
    )
    async def profile(
        self,
        interaction: discord.Interaction,
        member: discord.User = None
    ):
        member = member or interaction.user
        data = get_profile(member.id)

        progress = data["xp"] % 100
        filled = progress // 10
        bar = "🟩" * filled + "⬛" * (10 - filled)

        embed = discord.Embed(
            title=f"🏆 {member.display_name}'s Profile",
            description="Campus Chaos Player Card",
            color=discord.Color.gold()
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="⭐ Level",
            value=str(data["level"]),
            inline=True
        )

        embed.add_field(
            name="✨ Total XP",
            value=str(data["xp"]),
            inline=True
        )

        embed.add_field(
            name="📈 Progress",
            value=f"{bar}\n{progress}/100 XP",
            inline=False
        )

        embed.add_field(
            name="🎮 Commands Used",
            value=str(data["commands_used"]),
            inline=True
        )

        embed.add_field(
            name="🧠 Quiz Wins",
            value=str(data["quiz_wins"]),
            inline=True
        )

        await interaction.response.send_message(embed=embed)

    # ========================================
    # /leaderboard
    # ========================================

    @app_commands.command(
        name="leaderboard",
        description="View the Campus Chaos XP rankings"
    )
    async def leaderboard(
        self,
        interaction: discord.Interaction
    ):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT user_id, xp
                FROM users
                ORDER BY xp DESC, user_id ASC
                LIMIT 10
                """
            )

            players = cursor.fetchall()

        finally:
            conn.close()

        if not players:
            await interaction.response.send_message(
                "📭 Nobody has earned XP yet!"
            )
            return

        medals = ["🥇", "🥈", "🥉"]
        lines = []

        for index, (user_id, xp) in enumerate(players):
            medal = (
                medals[index]
                if index < 3
                else f"**{index + 1}.**"
            )

            lines.append(
                f"{medal} <@{user_id}> — **{xp} XP**"
            )

        embed = discord.Embed(
            title="🏆 Campus Chaos Leaderboard",
            description="\n".join(lines),
            color=discord.Color.gold()
        )

        embed.set_footer(
            text="Global rankings across all servers using this bot"
        )

        await interaction.response.send_message(embed=embed)

    # ========================================
    # /achievements
    # ========================================

    @app_commands.command(
        name="achievements",
        description="View your unlocked achievements"
    )
    async def achievements(
        self,
        interaction: discord.Interaction
    ):
        unlocked = get_achievements(interaction.user.id)

        embed = discord.Embed(
            title="🎖️ Your Achievements",
            description=(
                f"Unlocked {len(unlocked)} "
                f"of {len(ACHIEVEMENTS)} badges"
            ),
            color=discord.Color.purple()
        )

        for achievement_id, info in ACHIEVEMENTS.items():
            earned = achievement_id in unlocked

            embed.add_field(
                name=(
                    info["name"]
                    if earned
                    else f"🔒 {info['name']}"
                ),
                value=(
                    f"{info['description']}\n"
                    f"{'✅ Unlocked' if earned else '🔒 Locked'}"
                ),
                inline=False
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Levels(bot))
