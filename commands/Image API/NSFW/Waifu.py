import discord
from discord.ext import commands
import requests


class Waifu(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def waifu(self, ctx):
        response = requests.get('https://api.waifu.pics/nsfw/waifu')
        data = response.json()

        embed = discord.Embed(title="")
        embed.set_image(url=data['url'])

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Waifu(client))
