import discord
from discord.ext import commands
import asyncio


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        # Initial embed
        embed = discord.Embed(
            title="Help Oracle",
            description="React with the corresponding emojis to navigate between pages.",
            color=discord.Color.blue()
        )
        embed.add_field(name="1️⃣ Moderation", value="Moderation commands", inline=True)
        embed.add_field(name="2️⃣ Economy", value="Economy commands", inline=True)
        embed.add_field(name="3️⃣ Fun", value="Fun commands", inline=True)
        embed.add_field(name="4️⃣ Extra", value="Extra commands", inline=True)

        message = await ctx.send(embed=embed)

        # Add reactions
        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for emoji in emojis:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == message.id

        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)

                # Edit embed based on reaction
                if str(reaction.emoji) == '1️⃣':
                    embed.title = 'Moderation Commands'
                    embed.clear_fields()
                    embed.add_field(name="s!kick <mention user>", value=":boot: Kicks the specified user", inline=False)
                    embed.add_field(name="s!ban <mention user>", value=":hammer: Bans the specified user", inline=False)
                    embed.add_field(name="s!mute <mention user>", value=":mute: Mutes the specified user", inline=False)
                    embed.add_field(name="s!unmute <mention user>", value=":loud_sound: Unmutes the specified user",
                                    inline=False)
                    embed.add_field(name="s!clear <number>", value=":broom: Purges the specified amount of messages",
                                    inline=False)

                elif str(reaction.emoji) == '2️⃣':
                    embed.title = 'Economy Commands'
                    embed.clear_fields()
                    embed.add_field(name="s!balance", value=":money_with_wings: Check your * currency", inline=False)
                    embed.add_field(name="s!questing", value=":crossed_swords: Go questing to earn * currency",
                                    inline=False)

                elif str(reaction.emoji) == '4️⃣':
                    embed.title = 'Extra Commands'
                    embed.clear_fields()
                    embed.add_field(name="s!help", value=":information_source: Opens the Help Oracle", inline=False)
                    embed.add_field(name="s!setprefix <prefix>", value=":wrench: Allows you to change the current prefix", inline=False)

                # Repeat for other categories

                await message.edit(embed=embed)
                await reaction.remove(user)

            except asyncio.TimeoutError:
                break

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Cog Loaded Successfully")


async def setup(client):
    await client.add_cog(Help(client))
