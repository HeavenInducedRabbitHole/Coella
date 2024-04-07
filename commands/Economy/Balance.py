import discord
from discord.ext import commands
import json


class Balance(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Balance can be found")

    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        with open("jsons/economy.json", "r") as f:
            user_eco = json.load(f)

            if member is None:
                member = ctx.author
            elif member is not None:
                member = member

            if str(ctx.author.id) not in user_eco:
                user_eco[str(member.id)] = {}
                user_eco[str(member.id)]["Balance"] = 0

                with open("jsons/economy.json", "w") as f:
                    json.dump(user_eco, f, indent=4)

        eco_embed = discord.Embed(title=f"{member.name}'s Wealth", description="This users current networth",
                                  color=discord.Color.teal())
        eco_embed.add_field(name="Current Wealth:", value="*" + str(user_eco[str(member.id)]['Balance']))


        eco_embed.set_footer(text="May your day be filled with peace. | Saintess V:0.1")

        await ctx.send(embed=eco_embed)


async def setup(client):
    await client.add_cog(Balance(client))
