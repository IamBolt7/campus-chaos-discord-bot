
from database.db import get_connection


ACHIEVEMENTS = {
    "first_steps": {
        "name": "👶 First Steps",
        "description": "Use your first XP-earning command."
    },
    "touch_grass": {
        "name": "🌱 Touch Grass",
        "description": "Use 100 XP-earning commands."
    },
    "getting_started": {
        "name": "⭐ Getting Started",
        "description": "Reach Level 5."
    },
    "chaos_legend": {
        "name": "👑 Chaos Legend",
        "description": "Reach Level 20."
    },
    "quiz_master": {
        "name": "🧠 Quiz Master",
        "description": "Win 20 quizzes."
    }
}


def calculate_level(xp):
    # Level 1 begins at 0 XP.
    # Each additional level requires 100 XP.
    return (xp // 100) + 1


def add_xp(user_id, amount=10, quiz_win=False):
    user_id = str(user_id)

    if amount < 0:
        raise ValueError("XP amount cannot be negative.")

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO users (user_id)
            VALUES (?)
            """,
            (user_id,)
        )

        cursor.execute(
            """
            UPDATE users
            SET xp = xp + ?,
                commands_used = commands_used + 1,
                quiz_wins = quiz_wins + ?
            WHERE user_id = ?
            """,
            (amount, int(quiz_win), user_id)
        )

        cursor.execute(
            """
            SELECT xp, commands_used, quiz_wins
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        xp, commands_used, quiz_wins = cursor.fetchone()
        level = calculate_level(xp)

        unlocked = []

        conditions = {
            "first_steps": commands_used >= 1,
            "touch_grass": commands_used >= 100,
            "getting_started": level >= 5,
            "chaos_legend": level >= 20,
            "quiz_master": quiz_wins >= 20
        }

        for achievement_id, achieved in conditions.items():
            if not achieved:
                continue

            cursor.execute(
                """
                INSERT OR IGNORE INTO achievements
                (user_id, achievement_id)
                VALUES (?, ?)
                """,
                (user_id, achievement_id)
            )

            if cursor.rowcount > 0:
                unlocked.append(
                    ACHIEVEMENTS[achievement_id]["name"]
                )

        conn.commit()

        return {
            "xp": xp,
            "level": level,
            "commands_used": commands_used,
            "quiz_wins": quiz_wins,
            "unlocked": unlocked
        }

    finally:
        conn.close()


def get_profile(user_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT xp, commands_used, quiz_wins
            FROM users
            WHERE user_id = ?
            """,
            (str(user_id),)
        )

        row = cursor.fetchone()

        if not row:
            return {
                "xp": 0,
                "level": 1,
                "commands_used": 0,
                "quiz_wins": 0
            }

        xp, commands_used, quiz_wins = row

        return {
            "xp": xp,
            "level": calculate_level(xp),
            "commands_used": commands_used,
            "quiz_wins": quiz_wins
        }

    finally:
        conn.close()


def get_achievements(user_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT achievement_id
            FROM achievements
            WHERE user_id = ?
            """,
            (str(user_id),)
        )

        return {
            row[0] for row in cursor.fetchall()
        }

    finally:
        conn.close()
