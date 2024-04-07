import discord
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Clear can be found")

    @commands.command()
    async def clear(self, ctx, amount: int):
        # Check if the author has the necessary permission to manage messages
        if ctx.author.guild_permissions.manage_messages:
            # Add 1 to the amount to include the command message itself
            amount = min(amount + 1, 100)  # Limit to a maximum of 100 messages

            try:
                # Delete the messages
                deleted = await ctx.channel.purge(limit=amount)
                await ctx.send(f"Deleted {len(deleted) - 1} message(s).")
            except discord.Forbidden:
                await ctx.send("I don't have permission to delete messages.")
        else:
            await ctx.send("You don't have permission to manage messages.")


async def setup(client):
    await client.add_cog(Clear(client))
