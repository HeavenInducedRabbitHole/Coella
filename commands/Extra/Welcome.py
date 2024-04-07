import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

        @commands.Cog.listener()
        async def on_ready(self):
            print("Welcome system is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('Welcome to our Discord server!')


async def setup(client):
    await client.add_cog(Welcome(client))
