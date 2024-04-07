import discord
from discord.ext import commands
import asyncio
import random
from datetime import timedelta
import json
import os


class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.giveaways_file = "jsons/giveaways.json"
        if not os.path.exists(self.giveaways_file):
            with open(self.giveaways_file, 'w') as f:
                json.dump({}, f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Giveaway is ready")

    @commands.command()
    async def giveaway(self, ctx, time_unit, amount: int, *, prize):
        time_unit = time_unit.lower()

        if time_unit not in ['minutes', 'hours', 'days', 'weeks']:
            await ctx.send('Invalid time unit. Please use minutes/hours/days/weeks.')
            return

        if amount < 1:
            await ctx.send('Time amount must be at least 1.')
            return

        time_dict = {
            'minutes': timedelta(minutes=amount).total_seconds(),
            'hours': timedelta(hours=amount).total_seconds(),
            'days': timedelta(days=amount).total_seconds(),
            'weeks': timedelta(weeks=amount).total_seconds()
        }

        time_duration = time_dict[time_unit]

        embed = discord.Embed(title='🎉 Giveaway 🎉', description=prize, color=0x00ff00)
        embed.set_footer(text='This giveaway ends {} {} from now.'.format(amount, time_unit))
        giveaway_message = await ctx.send(embed=embed)
        await giveaway_message.add_reaction('🎉')

        # Save the giveaway
        with open(self.giveaways_file, 'r') as f:
            giveaways = json.load(f)
        giveaways[str(giveaway_message.id)] = {
            'channel_id': str(ctx.channel.id),
            'message_id': str(giveaway_message.id),
            'prize': prize,
            'duration': amount,
            'time_unit': time_unit
        }
        with open(self.giveaways_file, 'w') as f:
            json.dump(giveaways, f)

        await asyncio.sleep(time_duration)  # Sleep for the appropriate amount of seconds

        # get the message again to fetch the reactions
        giveaway_message = await ctx.channel.fetch_message(giveaway_message.id)
        for reaction in giveaway_message.reactions:
            if reaction.emoji == '🎉':
                users = await reaction.users().flatten()
                users.remove(self.client.user)
                if users:
                    winner = random.choice(users)
                    await ctx.send(f'Congratulations {winner.mention}! You won the **{prize}**!')
                else:
                    await ctx.send('Giveaway ended but no one reacted. 😞')

        # Remove the giveaway from the JSON file
        with open(self.giveaways_file, 'r') as f:
            giveaways = json.load(f)
        if str(giveaway_message.id) in giveaways:
            del giveaways[str(giveaway_message.id)]
        with open(self.giveaways_file, 'w') as f:
            json.dump(giveaways, f)


async def setup(client):
    await client.add_cog(Giveaway(client))
