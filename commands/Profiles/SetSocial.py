import json

import discord
from discord.ext import commands


class SetSocial(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Set Social can be found")

    @commands.command()
    async def add_social(self, ctx, platform, *, link):
        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        users[str(ctx.author.id)]["SocialLinks"][platform] = link

        with open("jsons/users.json", "w") as f:
            json.dump(users, f)

        await ctx.send(f"Your {platform} link has been added!")


async def setup(client):
    await client.add_cog(SetSocial(client))