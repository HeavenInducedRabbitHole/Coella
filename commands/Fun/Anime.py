import discord
from discord.ext import commands
import requests
import random


class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Anime system is ready.")

    @commands.command()
    async def random_anime(self, ctx):
        response = requests.get('https://api.jikan.moe/v3/top/anime/1/airing')
        data = response.json()
        anime_list = data['top']

        random.shuffle(anime_list)  # Randomize the order of the anime list
        selected_anime = anime_list[:10]  # Select the first 10 anime

        # Create an embed with the anime names
        embed = discord.Embed(title="Random Anime")
        for anime in selected_anime:
            embed.add_field(name=anime['title'], value='\u200b', inline=False)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Anime(client))
