import json
import random

import discord
from discord.ext import commands

class Work(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Work can be found")

    @commands.cooldown(1, 1800, commands.BucketType.user)  # 1800 seconds = 30 minutes
    @commands.command()
    async def work(self, ctx):
        # Define possible earnings and responses
        earnings = random.randint(10, 100)
        responses = [
            f"You butcher monster corpses and earn ${earnings}",
            f"You defeated some monsters while on a quest and earned ${earnings}",
            f"You sold otherworldly items to inhabitants and earned ${earnings}",
        ]

        # Select a random response
        response = random.choice(responses)

        # Load the user data
        with open("jsons/economy.json", "r") as f:
            users = json.load(f)

        # Add the earnings to the user's balance
        users[str(ctx.author.id)]['Balance'] += earnings

        # Save the updated user data
        with open("jsons/economy.json", "w") as f:
            json.dump(users, f)

        # Create an embed message
        embed = discord.Embed(
            title="Work Completed",
            description=response,
            color=discord.Color.green()
        )

        # Add balance field to the embed
        embed.add_field(name="Your New Balance", value=f"${users[str(ctx.author.id)]['Balance']}", inline=False)

        # Send the response
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Work(client))

