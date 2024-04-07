import datetime

import discord
from discord.ext import commands


class ServerInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ServerInfo is ready")

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name}",
            description="Server Information",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.teal()
        )
        embed.add_field(
            name="Server created at",
            value=f"{ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}"
        )
        embed.add_field(
            name="Members",
            value=f"{ctx.guild.member_count}"
        )
        embed.add_field(
            name="Owner",
            value=f"{ctx.guild.owner}"
        )
        embed.add_field(
            name="Preferred Locale",
            value=f"{ctx.guild.preferred_locale}"
        )
        embed.add_field(
            name="Text Channels",
            value=f"{len(ctx.guild.text_channels)}"
        )
        embed.add_field(
            name="Voice Channels",
            value=f"{len(ctx.guild.voice_channels)}"
        )
        embed.add_field(
            name="Number of Roles",
            value=f"{len(ctx.guild.roles)}"
        )
        embed.add_field(
            name="Is Large?",
            value=f"{'Yes' if ctx.guild.large else 'No'}"
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(ServerInfo(client))
