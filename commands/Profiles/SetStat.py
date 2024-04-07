import json

import discord
from discord.ext import commands


class SetStatus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Set Status can be found")

    @commands.command()
    async def set_status(self, ctx, *, status):
        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        users[str(ctx.author.id)]["Status"] = status

        with open("jsons/users.json", "w") as f:
            json.dump(users, f)

        await ctx.send("Your status has been set!")


async def setup(client):
    await client.add_cog(SetStatus(client))