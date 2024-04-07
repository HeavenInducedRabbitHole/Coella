import discord
from discord.ext import commands


class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Kick can be found")


    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} has been kicked.")
        else:
            await ctx.send("You don't have permission to kick members.")


async def setup(client):
    await client.add_cog(Kick(client))

