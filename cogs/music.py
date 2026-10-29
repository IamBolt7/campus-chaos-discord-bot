
import asyncio
import logging
from collections import deque
from dataclasses import dataclass
from urllib.parse import urlparse

import discord
import yt_dlp
from discord import app_commands
from discord.ext import commands


logger = logging.getLogger(__name__)

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
}


@dataclass
class Song:
    title: str
    page_url: str
    requester: str


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.current = {}
        self.locks = {}

    def get_queue(self, guild_id):
        return self.queues.setdefault(guild_id, deque())

    def get_lock(self, guild_id):
        if guild_id not in self.locks:
            self.locks[guild_id] = asyncio.Lock()
        return self.locks[guild_id]

    def extract_info(self, url):
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)

            if info and "entries" in info:
                info = next(
                    (entry for entry in info["entries"] if entry),
                    None
                )

            if not info:
                raise ValueError("No playable media found.")

            return info

    async def resolve_song(self, url, requester):
        info = await asyncio.to_thread(
            self.extract_info, url
        )

        return Song(
            title=info.get("title", "Unknown Song"),
            page_url=info.get("webpage_url") or url,
            requester=requester
        )

    async def get_stream_url(self, song):
        info = await asyncio.to_thread(
            self.extract_info, song.page_url
        )

        stream_url = info.get("url")

        if not stream_url:
            raise ValueError("No audio stream was returned.")

        return stream_url

    async def ensure_voice(self, interaction):
        guild = interaction.guild
        member = interaction.user

        if not guild or not isinstance(member, discord.Member):
            raise ValueError(
                "This command only works inside a server."
            )

        if not member.voice or not member.voice.channel:
            raise ValueError(
                "Join a voice channel first! 🎧"
            )

        channel = member.voice.channel
        voice = guild.voice_client

        if voice and voice.is_connected():
            if voice.channel != channel:
                raise ValueError(
                    "Join my current voice channel first."
                )
            return voice

        permissions = channel.permissions_for(guild.me)

        if not permissions.connect or not permissions.speak:
            raise ValueError(
                "I need Connect and Speak permissions."
            )

        return await channel.connect()

    async def require_same_channel(self, interaction):
        guild = interaction.guild

        if not guild or not guild.voice_client:
            raise ValueError("I'm not in a voice channel.")

        voice = guild.voice_client

        if not voice.is_connected():
            raise ValueError("I'm not connected to voice.")

        member = interaction.user

        if (
            not isinstance(member, discord.Member)
            or not member.voice
            or member.voice.channel != voice.channel
        ):
            raise ValueError(
                "Join my voice channel to control the music."
            )

        return voice

    async def play_next(self, guild_id):
        lock = self.get_lock(guild_id)

        async with lock:
            guild = self.bot.get_guild(guild_id)

            if not guild or not guild.voice_client:
                self.current.pop(guild_id, None)
                return

            voice = guild.voice_client

            if not voice.is_connected():
                self.current.pop(guild_id, None)
                return

            if voice.is_playing() or voice.is_paused():
                return

            queue = self.get_queue(guild_id)

            while queue:
                song = queue.popleft()

                try:
                    stream_url = await self.get_stream_url(song)

                    source = discord.FFmpegPCMAudio(
                        stream_url,
                        before_options=(
                            "-reconnect 1 "
                            "-reconnect_streamed 1 "
                            "-reconnect_delay_max 5"
                        ),
                        options="-vn"
                    )

                    self.current[guild_id] = song

                    def after_playback(error):
                        if error:
                            logger.error(
                                "Music playback error: %s", error
                            )

                        future = asyncio.run_coroutine_threadsafe(
                            self.finish_song(guild_id),
                            self.bot.loop
                        )

                        def log_future(f):
                            try:
                                f.result()
                            except Exception:
                                logger.exception(
                                    "Could not advance music queue"
                                )

                        future.add_done_callback(log_future)

                    voice.play(
                        source,
                        after=after_playback
                    )
                    return

                except Exception:
                    logger.exception(
                        "Could not play: %s", song.title
                    )

            self.current.pop(guild_id, None)

    async def finish_song(self, guild_id):
        self.current.pop(guild_id, None)
        await self.play_next(guild_id)

    # ==========================================
    # /join
    # ==========================================

    @app_commands.command(
        name="join",
        description="Join your voice channel"
    )
    async def join(self, interaction: discord.Interaction):
        try:
            voice = await self.ensure_voice(interaction)
            await interaction.response.send_message(
                f"🎧 Joined **{voice.channel.name}**!"
            )
        except (ValueError, discord.DiscordException) as error:
            await interaction.response.send_message(
                f"❌ {error}", ephemeral=True
            )

    # ==========================================
    # /play
    # ==========================================

    @app_commands.command(
        name="play",
        description="Play audio from a supported media URL"
    )
    @app_commands.describe(
        url="A supported media-page or direct audio URL"
    )
    async def play(
        self,
        interaction: discord.Interaction,
        url: str
    ):
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            await interaction.response.send_message(
                "❌ Please provide a valid HTTPS media URL.",
                ephemeral=True
            )
            return

        await interaction.response.defer()

        try:
            voice = await self.ensure_voice(interaction)

            song = await self.resolve_song(
                url,
                interaction.user.display_name
            )

            guild_id = interaction.guild.id
            queue = self.get_queue(guild_id)

            queue.append(song)

            await self.play_next(guild_id)

            if self.current.get(guild_id) is song:
                status = "▶️ Now Playing"
            else:
                status = "📥 Added to Queue"

            embed = discord.Embed(
                title=status,
                description=f"**{song.title}**",
                color=discord.Color.blurple()
            )

            embed.add_field(
                name="Requested by",
                value=song.requester
            )

            embed.add_field(
                name="Voice Channel",
                value=voice.channel.name
            )

            await interaction.followup.send(embed=embed)

        except Exception as error:
            logger.exception("Play command failed")
            await interaction.followup.send(
                f"❌ Unable to play this source: {error}",
                ephemeral=True
            )

    # ==========================================
    # /pause
    # ==========================================

    @app_commands.command(
        name="pause",
        description="Pause the current song"
    )
    async def pause(self, interaction: discord.Interaction):
        try:
            voice = await self.require_same_channel(interaction)

            if not voice.is_playing():
                raise ValueError("Nothing is currently playing.")

            voice.pause()

            await interaction.response.send_message(
                "⏸️ Music paused."
            )

        except ValueError as error:
            await interaction.response.send_message(
                f"❌ {error}", ephemeral=True
            )

    # ==========================================
    # /resume
    # ==========================================

    @app_commands.command(
        name="resume",
        description="Resume paused music"
    )
    async def resume(self, interaction: discord.Interaction):
        try:
            voice = await self.require_same_channel(interaction)

            if not voice.is_paused():
                raise ValueError("Music is not paused.")

            voice.resume()

            await interaction.response.send_message(
                "▶️ Music resumed."
            )

        except ValueError as error:
            await interaction.response.send_message(
                f"❌ {error}", ephemeral=True
            )

    # ==========================================
    # /skip
    # ==========================================

    @app_commands.command(
        name="skip",
        description="Skip the current song"
    )
    async def skip(self, interaction: discord.Interaction):
        try:
            voice = await self.require_same_channel(interaction)

            if not (voice.is_playing() or voice.is_paused()):
                raise ValueError("Nothing to skip.")

            voice.stop()

            await interaction.response.send_message(
                "⏭️ Song skipped!"
            )

        except ValueError as error:
            await interaction.response.send_message(
                f"❌ {error}", ephemeral=True
            )

    # ==========================================
    # /queue
    # ==========================================

    @app_commands.command(
        name="queue",
        description="View upcoming songs"
    )
    async def queue(self, interaction: discord.Interaction):
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Server only.", ephemeral=True
            )
            return

        songs = list(self.get_queue(interaction.guild.id))

        if not songs:
            await interaction.response.send_message(
                "📭 The music queue is empty."
            )
            return

        lines = [
            f"**{index}.** {song.title} — {song.requester}"
            for index, song in enumerate(songs[:10], start=1)
        ]

        embed = discord.Embed(
            title="🎶 Music Queue",
            description="\n".join(lines),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed)

    # ==========================================
    # /nowplaying
    # ==========================================

    @app_commands.command(
        name="nowplaying",
        description="Show the current song"
    )
    async def nowplaying(
        self,
        interaction: discord.Interaction
    ):
        if not interaction.guild:
            await interaction.response.send_message(
                "❌ Server only.", ephemeral=True
            )
            return

        song = self.current.get(interaction.guild.id)

        if not song:
            await interaction.response.send_message(
                "🔇 Nothing is currently playing."
            )
            return

        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{song.title}**",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Requested by",
            value=song.requester
        )

        await interaction.response.send_message(embed=embed)

    # ==========================================
    # /stop
    # ==========================================

    @app_commands.command(
        name="stop",
        description="Stop music and leave voice"
    )
    async def stop(self, interaction: discord.Interaction):
        try:
            voice = await self.require_same_channel(interaction)

            guild_id = interaction.guild.id

            self.get_queue(guild_id).clear()
            self.current.pop(guild_id, None)

            # Disconnect before stopping playback so
            # the callback cannot start another song.
            await voice.disconnect(force=True)

            await interaction.response.send_message(
                "🛑 Music stopped. Queue cleared. Goodbye! 👋"
            )

        except ValueError as error:
            await interaction.response.send_message(
                f"❌ {error}", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Music(bot))
