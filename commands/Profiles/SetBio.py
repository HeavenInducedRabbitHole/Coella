import json

import discord
from discord.ext import commands


class SetBio(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Set Bio can be found")

    @commands.command()
    async def set_bio(self, ctx, *, bio):
        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        users[str(ctx.author.id)]["Bio"] = bio

        with open("jsons/users.json", "w") as f:
            json.dump(users, f)

        await ctx.send("Your bio has been set!")


async def setup(client):
    await client.add_cog(SetBio(client))