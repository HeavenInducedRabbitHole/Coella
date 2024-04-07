import discord
from discord.ext import commands


class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ban can be found")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned from this world.")
        else:
            await ctx.send("You don't have the authority to ban members.")


async def setup(client):
    await client.add_cog(Ban(client))

