import discord
from discord import app_commands
from discord.ext import commands

from database.db import get_connection


class Attendance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # =========================================================
    # /subject
    # Add a new subject
    # =========================================================

    @app_commands.command(
        name="subject",
        description="Add a subject to your attendance tracker"
    )
    async def subject(
        self,
        interaction: discord.Interaction,
        name: str,
        attended: int,
        total: int,
        required_percentage: float = 75.0
    ):

        # Validate values
        if attended < 0 or total < 0:
            await interaction.response.send_message(
                "❌ Attendance values cannot be negative.",
                ephemeral=True
            )
            return

        if attended > total:
            await interaction.response.send_message(
                "❌ Attended classes cannot be greater than total classes.",
                ephemeral=True
            )
            return

        if required_percentage <= 0 or required_percentage > 100:
            await interaction.response.send_message(
                "❌ Required percentage must be between 1 and 100.",
                ephemeral=True
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO subjects
                (
                    user_id,
                    subject_name,
                    attended,
                    total,
                    required_percentage
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(interaction.user.id),
                    name,
                    attended,
                    total,
                    required_percentage
                )
            )

            conn.commit()

            percentage = (
                attended / total * 100
                if total > 0
                else 0
            )

            await interaction.response.send_message(
                f"""
📚 **Subject Added!**

**{name}**

Classes attended: `{attended}`
Total classes: `{total}`
Attendance: **{percentage:.1f}%**
Required: `{required_percentage:.1f}%`
"""
            )

        except Exception:
            await interaction.response.send_message(
                f"⚠️ `{name}` already exists in your subjects.",
                ephemeral=True
            )

        finally:
            conn.close()

    # =========================================================
    # /attendance
    # View all subjects
    # =========================================================

    @app_commands.command(
        name="attendance",
        description="View your attendance"
    )
    async def attendance(
        self,
        interaction: discord.Interaction
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                subject_name,
                attended,
                total,
                required_percentage
            FROM subjects
            WHERE user_id = ?
            """,
            (str(interaction.user.id),)
        )

        subjects = cursor.fetchall()

        conn.close()

        if not subjects:
            await interaction.response.send_message(
                "📭 You haven't added any subjects yet.\n\n"
                "Use `/subject` first.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📊 Your Attendance",
            description="Your current academic survival status."
        )

        for name, attended, total, required in subjects:

            percentage = (
                attended / total * 100
                if total > 0
                else 0
            )

            if percentage >= 90:
                status = "🗿 Bro attends classes recreationally."

            elif percentage >= 85:
                status = "🤓 Professor's favourite student."

            elif percentage >= 80:
                status = "😎 Plenty of breathing room."

            elif percentage >= required + 3:
                status = "😏 Bunking privileges unlocked."

            elif percentage >= required:
                status = "⚠️ One wrong move and you're cooked."

            elif percentage >= 60:
                status = "💀 Academic comeback arc begins."

            else:
                status = "🪦 Your attendance needs CPR."

            embed.add_field(
                name=f"📚 {name}",
                value=(
                    f"Attendance: **{percentage:.1f}%**\n"
                    f"Classes: `{attended}/{total}`\n"
                    f"Required: `{required:.1f}%`\n"
                    f"{status}"
                ),
                inline=False
            )

        await interaction.response.send_message(
            embed=embed
        )

    # =========================================================
    # /attend
    # Mark a class as attended
    # =========================================================

    @app_commands.command(
        name="attend",
        description="Mark a class as attended"
    )
    async def attend(
        self,
        interaction: discord.Interaction,
        subject: str
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT attended, total
            FROM subjects
            WHERE user_id = ?
            AND LOWER(subject_name) = LOWER(?)
            """,
            (
                str(interaction.user.id),
                subject
            )
        )

        data = cursor.fetchone()

        if not data:
            conn.close()

            await interaction.response.send_message(
                f"❌ I couldn't find `{subject}`.",
                ephemeral=True
            )
            return

        attended, total = data

        # Attended class means both values increase
        attended += 1
        total += 1

        cursor.execute(
            """
            UPDATE subjects
            SET attended = ?, total = ?
            WHERE user_id = ?
            AND LOWER(subject_name) = LOWER(?)
            """,
            (
                attended,
                total,
                str(interaction.user.id),
                subject
            )
        )

        conn.commit()
        conn.close()

        percentage = attended / total * 100

        await interaction.response.send_message(
            f"""
✅ **Class Attended!**

📚 **{subject}**

Attendance: `{attended}/{total}`
Percentage: **{percentage:.1f}%**

Look at you actually attending college. 🗿
"""
        )

    # =========================================================
    # /bunk
    # Mark a class as bunked
    # =========================================================

    @app_commands.command(
        name="bunk",
        description="Mark a class as bunked"
    )
    async def bunk(
        self,
        interaction: discord.Interaction,
        subject: str
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT attended, total, required_percentage
            FROM subjects
            WHERE user_id = ?
            AND LOWER(subject_name) = LOWER(?)
            """,
            (
                str(interaction.user.id),
                subject
            )
        )

        data = cursor.fetchone()

        if not data:
            conn.close()

            await interaction.response.send_message(
                f"❌ I couldn't find `{subject}`.",
                ephemeral=True
            )
            return

        attended, total, required = data

        old_percentage = (
            attended / total * 100
            if total > 0
            else 0
        )

        # Bunking increases total classes
        # but NOT attended classes.
        total += 1

        cursor.execute(
            """
            UPDATE subjects
            SET total = ?
            WHERE user_id = ?
            AND LOWER(subject_name) = LOWER(?)
            """,
            (
                total,
                str(interaction.user.id),
                subject
            )
        )

        conn.commit()
        conn.close()

        new_percentage = attended / total * 100

        if new_percentage >= required:
            status = "😎 You're still safe."
        else:
            status = "🚨 YOU'RE BELOW THE REQUIRED ATTENDANCE."

        await interaction.response.send_message(
            f"""
💀 **Class Bunked**

📚 **{subject}**

Before: **{old_percentage:.1f}%**
After: **{new_percentage:.1f}%**

{status}
"""
        )

    # =========================================================
    # /canibunk
    # Calculate safe bunks
    # =========================================================

    @app_commands.command(
        name="canibunk",
        description="Calculate how many classes you can safely bunk"
    )
    async def canibunk(
        self,
        interaction: discord.Interaction,
        subject: str
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT attended, total, required_percentage
            FROM subjects
            WHERE user_id = ?
            AND LOWER(subject_name) = LOWER(?)
            """,
            (
                str(interaction.user.id),
                subject
            )
        )

        data = cursor.fetchone()

        conn.close()

        if not data:
            await interaction.response.send_message(
                f"❌ I couldn't find `{subject}`.",
                ephemeral=True
            )
            return

        attended, total, required = data

        if total == 0:
            await interaction.response.send_message(
                "⚠️ You haven't recorded any classes yet."
            )
            return

        current = attended / total * 100

        safe_bunks = 0

        while (
            attended /
            (total + safe_bunks + 1)
            * 100
            >= required
        ):
            safe_bunks += 1

        # User cannot safely bunk
        if safe_bunks == 0:

            next_percentage = (
                attended /
                (total + 1)
                * 100
            )

            message = f"""
🚨 **DO NOT BUNK**

📚 **{subject}**

Current attendance: **{current:.1f}%**
Required attendance: **{required:.1f}%**

If you bunk the next class:
**{next_percentage:.1f}%**

You cannot safely bunk the next class.

**GO TO CLASS. 💀**
"""

        # User can safely bunk
        else:

            after_bunking = (
                attended /
                (total + safe_bunks)
                * 100
            )

            message = f"""
😈 **BUNK CALCULATOR**

📚 **{subject}**

Current attendance: **{current:.1f}%**
Required attendance: **{required:.1f}%**

🔥 You can safely bunk **{safe_bunks} class(es)**.

Attendance afterwards:
**{after_bunking:.1f}%**

🟢 **SAFE TO BUNK**
"""

        await interaction.response.send_message(
            message
        )


# =============================================================
# Load Attendance Cog
# =============================================================

async def setup(bot):
    await bot.add_cog(Attendance(bot))