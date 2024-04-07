import discord
from discord.ext import commands


class Unmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Unmute can be found")

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        # Check if the author has the necessary permission to unmute members
        if ctx.author.guild_permissions.mute_members:
            # Get the "Muted" role
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if muted_role:
                # Check if the member has the "Muted" role before removing it
                if muted_role in member.roles:
                    await member.remove_roles(muted_role)
                    await ctx.send(f"{member.mention} has been unmuted.")
                else:
                    await ctx.send(f"{member.mention} is not muted.")
            else:
                await ctx.send("There is no 'Muted' role in this server.")
        else:
            await ctx.send("You don't have permission to unmute members.")


async def setup(client):
    await client.add_cog(Unmute(client))
