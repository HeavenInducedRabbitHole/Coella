import discord
from discord.ext import commands


class SecretMessage(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.authorized_ids = [942894031329955850, 569975518133354549, 1012863055543160852]  # Replace with your actual authorized user IDs

    @commands.Cog.listener()
    async def on_ready(self):
        print("Secret Message can be found")

    @commands.command()
    async def loveletter(self, ctx, member: discord.Member, *, message):
        if ctx.author.id not in self.authorized_ids:
            await ctx.send("Sorry, you are not authorized to use this command.")
            return

        await ctx.message.delete()

        # Create an embed for the message
        embed = discord.Embed(title="💌 You've Received A Love Letter(or not?) 💌", description=message,
                              color=discord.Color.pink())
        await member.send(embed=embed)

        # Confirmation message
        confirmation_embed = discord.Embed(title="Message Sent Anonymously",
                                           description="Your message has been sent anonymously.",
                                           color=discord.Color.pink())
        await ctx.send(embed=confirmation_embed)


async def setup(client):
    await client.add_cog(SecretMessage(client))
