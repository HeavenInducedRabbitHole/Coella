import discord
from discord.ext import commands


class Filter(commands.Cog):
    def __init__(self, client):
        self.client = client
        # A list of forbidden words that you want to filter.
        self.forbidden_words = ["Fuck", "Shit", "Idiot"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if any(forbidden_word in message.content for forbidden_word in self.forbidden_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Do everyone a favor and refrain from using such language.")

    @commands.command()
    async def banword(self, ctx, word: str):
        if word not in self.forbidden_words:
            self.forbidden_words.append(word)
            await ctx.send(f"Word '{word}' added to banned word list.")

    @commands.command()
    async def unbanword(self, ctx, word: str):
        if word in self.forbidden_words:
            self.forbidden_words.remove(word)
            await ctx.send(f"Word '{word}' removed from banned word list.")


async def setup(client):
    await client.add_cog(Filter(client))
