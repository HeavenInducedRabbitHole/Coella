import discord
from discord.ext import commands
import json
import os


class Faith(commands.Cog):
    def __init__(self, client):
        self.client = client
        if not os.path.exists('jsons/faith.json'):  # creates faith.json if it does not exist
            with open('jsons/faith.json', 'w') as f:
                json.dump({}, f)
        with open('jsons/faith.json', 'r') as f:
            self.faiths = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Faith system is ready.")

    @commands.command()
    async def faith(self, ctx, member: discord.Member):
        # check faith of the user
        user_id = str(member.id)
        faith = self.faiths.get(user_id, 0)

        # create an embed message
        embed = discord.Embed(title="Faith Points", color=discord.Color.yellow())
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Faith Points", value=faith, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def givefaith(self, ctx, member: discord.Member):
        # give faith to the user
        user_id = str(member.id)
        self.faiths[user_id] = self.faiths.get(user_id, 0) + 1
        with open('jsons/faith.json', 'w') as f:
            json.dump(self.faiths, f)

        # create an embed message
        embed = discord.Embed(title="Faith Given", color=discord.Color.teal())
        embed.add_field(name="Faith Giver", value=ctx.author.mention, inline=False)
        embed.add_field(name="Receiver", value=member.mention, inline=False)
        embed.add_field(name="New Faith Points", value=self.faiths[user_id], inline=False)

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Faith(client))
