import json
import re

import discord
from discord.ext import commands


class SetBackground(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Set Background can be found")

    @commands.command()
    async def set_background(self, ctx, *, url):
        # Check if the provided string is a valid URL
        if not re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
            await ctx.send("Please provide a valid URL.")
            return

        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        users[str(ctx.author.id)]["Background"] = url

        with open("jsons/users.json", "w") as f:
            json.dump(users, f)

        await ctx.send("Your background has been set!")


async def setup(client):
    await client.add_cog(SetBackground(client))