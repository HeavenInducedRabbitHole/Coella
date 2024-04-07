import json
import random

import discord
from discord.ext import commands


class Badges(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Badges can be found")

    @commands.command()
    async def badges(self, ctx):
        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        user = users[str(ctx.author.id)]

        # Check if the user has used the command 10 times
        if user["CommandsUsed"] >= 10 and "10 Commands Used" not in user["Badges"]:
            user["Badges"].append("10 Commands Used")
            await ctx.send("Congratulations! You've earned the '10 Commands Used' badge!")

        with open("jsons/users.json", "w") as f:
            json.dump(users, f)


async def setup(client):
    await client.add_cog(Badges(client))
