import discord
from discord.ext import commands


class UserInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("UserInfo is ready")

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        roles = [role for role in member.roles]
        embed = discord.Embed(color=discord.Color.teal(), timestamp=ctx.message.created_at)
        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Guild name:", value=member.display_name)
        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Roles:", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top role:", value=member.top_role.mention)
        embed.add_field(name="Status:", value=str(member.status))
        embed.add_field(name="Activity:", value=str(member.activity))
        embed.add_field(name="Is a Bot:", value=str(member.bot))
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(UserInfo(client))
