import discord
import json
import asyncio
from discord.ext import commands


class CurrencyLeaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Currency leaderboard is ready")

    @commands.command()
    async def currency_leaderboard(self, ctx):
        with open('jsons/economy.json', 'r') as f:
            data = json.load(f)

        # Sort the data according to economy balance
        sorted_data = sorted(data.items(), key=lambda x: x[1]['Balance'], reverse=True)

        # Create a list of embeds
        embeds = []
        for i in range(0, len(sorted_data), 10):
            embed = discord.Embed(title="* Leaderboard", color=discord.Color.green())
            for item in sorted_data[i:i + 10]:
                try:
                    user = await self.client.fetch_user(int(item[0]))
                    embed.add_field(
                        name=f"{i + 1}. {user.name if user else 'Unknown#0000'}",
                        value=f"Balance: *{item[1]['Balance']}",
                        inline=False
                    )
                except discord.NotFound as e:
                    print(f"User {item[0]} not found")
            embeds.append(embed)

        # Send the first page
        message = await ctx.send(embed=embeds[0])

        # Add reactions
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        i = 0
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and i + 1 < len(embeds):
                    i += 1
                    await message.edit(embed=embeds[i])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and i > 0:
                    i -= 1
                    await message.edit(embed=embeds[i])
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                break

        # Remove reactions
        await message.clear_reactions()


async def setup(client):
    await client.add_cog(CurrencyLeaderboard(client))


