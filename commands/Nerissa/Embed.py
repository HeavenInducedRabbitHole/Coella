import discord
from discord.ext import commands
import asyncio

class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Embed can be found")

    @commands.command()
    async def embed(self, ctx):
        options = ['Option 1', 'Option 2', 'Option 3']
        await self.send_options_and_wait_for_choice(ctx, options)

    async def send_options_and_wait_for_choice(self, ctx, options, timeout=60.0):
        embed = discord.Embed(title="Choose an option",
                              description='\n'.join(options),
                              color=discord.Color.green())
        await ctx.send(embed=embed)

        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content in options

        try:
            msg = await self.client.wait_for('message', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Sorry, you took too long to choose an option.')
        else:
            await ctx.send('It works')

async def setup(client):
    await client.add_cog(Embed(client))
