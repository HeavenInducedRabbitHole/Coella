import json
import re

import discord
from discord.ext import commands


class SetColor(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Set Color can be found")

    @commands.command()
    async def set_color(self, ctx, color: str):
        # Check if the provided string is a valid hex color
        if not re.match(r'^[A-Fa-f0-9]{6}$', color):
            await ctx.send("Please provide a valid hex color (6 digits, for example 'FFFFFF' for white).")
            return

        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        users[str(ctx.author.id)]["EmbedColor"] = color

        with open("jsons/users.json", "w") as f:
            json.dump(users, f)

        await ctx.send("Your embed color has been set!")


async def setup(client):
    await client.add_cog(SetColor(client))