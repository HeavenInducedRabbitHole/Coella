import discord
from discord.ext import commands
import json
from datetime import datetime, timedelta

class Marriage(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.load_marriages()

    def load_marriages(self):
        with open('jsons/relationship.json', 'r') as f:
            self.marriages = json.load(f)

    def save_marriages(self):
        with open('jsons/relationship.json', 'w') as f:
            json.dump(self.marriages, f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Marriage system is ready.")

    @commands.command()
    async def propose(self, ctx, user: discord.Member):
        await ctx.send(
            f"{ctx.author.mention} has proposed to {user.mention}! Type `{ctx.prefix}accept {ctx.author.id}` to accept!")

    @commands.command()
    async def accept(self, ctx, proposer: discord.Member):
        if f"{ctx.author.id}-{proposer.id}" not in self.marriages and f"{proposer.id}-{ctx.author.id}" not in self.marriages:
            self.marriages[f"{ctx.author.id}-{proposer.id}"] = datetime.now().isoformat()
            self.save_marriages()
            await ctx.send(f"{ctx.author.mention} and {proposer.mention} are now married!")
        else:
            await ctx.send("You're already married!")

    @commands.command()
    async def divorce(self, ctx, user: discord.Member):
        if f"{ctx.author.id}-{user.id}" in self.marriages:
            del self.marriages[f"{ctx.author.id}-{user.id}"]
            self.save_marriages()
            await ctx.send(f"{ctx.author.mention} and {user.mention} are now divorced.")
        elif f"{user.id}-{ctx.author.id}" in self.marriages:
            del self.marriages[f"{user.id}-{ctx.author.id}"]
            self.save_marriages()
            await ctx.send(f"{ctx.author.mention} and {user.mention} are now divorced.")
        else:
            await ctx.send("You're not married to this user!")

    @commands.command()
    async def marriageinfo(self, ctx, user: discord.Member):
        if f"{ctx.author.id}-{user.id}" in self.marriages:
            marriage_date = datetime.fromisoformat(self.marriages[f"{ctx.author.id}-{user.id}"])
        elif f"{user.id}-{ctx.author.id}" in self.marriages:
            marriage_date = datetime.fromisoformat(self.marriages[f"{user.id}-{ctx.author.id}"])
        else:
            await ctx.send("You're not married to this user!")
            return

        length = datetime.now() - marriage_date + timedelta(days=0)  # Add a day
        years, remainder = divmod(length.total_seconds(), 31536000)
        months, remainder = divmod(remainder, 2592000)
        days, _ = divmod(remainder, 86400)

        embed = discord.Embed(
            title="Marriage Info",
            description=f"{ctx.author.mention} and {user.mention} have been married!",
            color=discord.Color.pink()
        )
        embed.add_field(name="Marriage Date", value=marriage_date.strftime("%d/%m/%Y"), inline=False)
        embed.add_field(name="Duration", value=f"{int(years)} years, {int(months)} months, {int(days)} days", inline=False)
        embed.set_footer(text="May you be married for eternity.")
        embed.timestamp = datetime.utcnow()

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Marriage(client))
