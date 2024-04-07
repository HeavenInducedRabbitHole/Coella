import discord
from discord.ext import commands
import asyncio
import json
import Data

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info cog ready")


@commands.command()
async def skill_info(self, ctx, skill_name):
    if skill_name in self.skills:
        skill = self.skills[skill_name]
        await ctx.send(
            f"{skill_name}: {skill['description']}\nDamage: {skill.get('damage', 'N/A')}\nHealing: {skill.get('healing', 'N/A')}")
    else:
        await ctx.send("Unknown skill.")


@commands.command()
async def race_info(self, ctx, race_name):
    if race_name in self.race_info:
        await ctx.send(
            f"Race: {race_name}\nLifespan: {self.race_info[race_name]['lifespan']}\nMax age: {self.race_info[race_name]['max_age']}")
    else:
        await ctx.send("Unknown race.")


async def setup(client):
    await client.add_cog(Info(client))
