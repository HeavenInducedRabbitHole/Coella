import discord
from discord.ext import commands


class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Avatar is ready")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        embed = discord.Embed(color=discord.Color.green(), timestamp=ctx.message.created_at)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Avatar(client))
