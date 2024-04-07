import discord
from discord.ext import commands
import asyncio
import json

class Register(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.races = ["Elf", "Human", "Orc", "Dwarf"]
        self.genders = ["Male", "Female"]
        self.stats = ["Strength", "Defense", "Agility", "Knowledge", "Charm"]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Register cog ready")

    @commands.command()
    async def register(self, ctx):
        await ctx.send('Please type your first name.')
        first_name = await self.get_response(ctx)

        await ctx.send('Please type your gender.')
        gender = await self.get_response(ctx, self.genders)

        await ctx.send('Choose your race.')
        race = await self.get_response(ctx, self.races)

        await ctx.send('Allocate 10 stat points between Strength, Defense, Agility, Knowledge and Charm. For example: Strength 5, Charm 5')
        stats = await self.get_stats(ctx)

        data = {
            "first_name": first_name,
            "gender": gender,
            "race": race,
            "stats": stats
        }
        with open('jsons/nerissa.json', 'r') as f:
            users = json.load(f)
        users[str(ctx.author.id)] = data
        with open('jsons/nerissa.json', 'w') as f:
            json.dump(users, f)

        await ctx.send('Enjoy your new life in Nerissa')

    async def get_response(self, ctx, options=None, timeout=60.0):
        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and (options is None or m.content in options)

        try:
            msg = await self.client.wait_for('message', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Sorry, you took too long.')
            return None
        else:
            return msg.content

    async def get_stats(self, ctx):
        stat_points = {}
        while sum(stat_points.values()) != 10:
            response = await self.get_response(ctx)
            if response is None:
                return None
            stat_points = {stat.split(' ')[0]: int(stat.split(' ')[1]) for stat in response.split(', ')}
            if sum(stat_points.values()) > 10 or any(stat not in self.stats for stat in stat_points.keys()):
                await ctx.send('Invalid stat distribution. Please make sure you are distributing exactly 10 points among Strength, Defense, Agility, Knowledge and Charm.')
                stat_points = {}
        return stat_points

async def setup(client):
    await client.add_cog(Register(client))
