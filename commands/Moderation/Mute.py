import discord
from discord.ext import commands


class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mute can be found")

    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        # Check if the author has the necessary permission to mute members
        if ctx.author.guild_permissions.mute_members:
            # Get the "Muted" role or create it if it doesn't exist
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await ctx.guild.create_role(name="Muted")

            # Add the "Muted" role to the member
            await member.add_roles(muted_role, reason=reason)
            await ctx.send(f"{member.mention} has been muted.")
        else:
            await ctx.send("You don't have permission to mute members.")


async def setup(client):
    await client.add_cog(Mute(client))
