import json

import discord
from discord.ext import commands

class Level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Work can be found")

    @commands.command(pass_context=True)
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        with open('jsons/level.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(member.id)]['level']
        exp = users[str(member.id)]['experience']

        await ctx.send(f'{member.mention} is at level {lvl} with {exp} EXP.')


async def setup(client):
    await client.add_cog(Level(client))
