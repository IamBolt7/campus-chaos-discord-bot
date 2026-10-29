import discord
from discord.ext import commands
import aiohttp


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="meme",
        description="Get a random meme 😂"
    )
    async def meme(self, interaction: discord.Interaction):

        # Discord interactions must be acknowledged quickly.
        await interaction.response.defer()

        url = "https://meme-api.com/gimme"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:

                    if response.status != 200:
                        await interaction.followup.send(
                            "💀 The meme machine broke. Try again!"
                        )
                        return

                    data = await response.json()

            title = data.get("title", "Random Meme")
            meme_url = data.get("url")
            subreddit = data.get("subreddit", "memes")

            if not meme_url:
                await interaction.followup.send(
                    "💀 I found a meme with no image. Impressive."
                )
                return

            embed = discord.Embed(
                title=f"😂 {title}",
                color=discord.Color.orange()
            )

            embed.set_image(url=meme_url)

            embed.set_footer(
                text=f"r/{subreddit} • Campus Chaos"
            )

            await interaction.followup.send(embed=embed)

        except Exception as error:
            print(f"Meme error: {error}")

            await interaction.followup.send(
                "💀 Something went wrong while stealing memes "
                "from the internet."
            )


async def setup(bot):
    await bot.add_cog(Memes(bot))