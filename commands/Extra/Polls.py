import discord
from discord.ext import commands
import asyncio
import json
import os


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.polls_file = "jsons/polls.json"
        if not os.path.exists(self.polls_file):
            with open(self.polls_file, 'w') as f:
                json.dump({}, f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Poll is ready")

    @commands.command()
    async def poll(self, ctx, minutes: int, *, params):
        params = [p.strip() for p in params.split(',')]
        if len(params) <= 1:
            await ctx.send('A poll must have more than one option.')
            return
        if len(params) > 11:  # includes the title
            await ctx.send('You cannot have more than 10 options.')
            return

        question = params[0]
        options = params[1:]

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description), color=discord.Color.teal())

        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)

        # Save the poll
        with open(self.polls_file, 'r') as f:
            polls = json.load(f)
        polls[str(react_message.id)] = {
            'channel_id': str(ctx.channel.id),
            'message_id': str(react_message.id),
            'question': question,
            'options': options,
            'duration': minutes
        }
        with open(self.polls_file, 'w') as f:
            json.dump(polls, f)

        await asyncio.sleep(minutes * 60)  # convert minutes to seconds

        # Fetch the message again after poll has ended to get the reactions
        react_message = await ctx.channel.fetch_message(react_message.id)

        # Tally the votes
        total_votes = 0
        react_counts = {}
        for reaction in react_message.reactions:
            if reaction.emoji in reactions:
                react_counts[reaction.emoji] = reaction.count - 1  # exclude the bot's vote
                total_votes += reaction.count - 1

        # Build the results description
        results_desc = []
        for x, option in enumerate(options):
            count = react_counts.get(reactions[x], 0)
            if total_votes > 0:
                percent = count / total_votes * 100
            else:
                percent = 0
            results_desc += '\n{} {} - {} vote(s) ({:.2f}%)'.format(reactions[x], option, count, percent)

        embed = discord.Embed(title="Poll ended: {}".format(question),
                              description=''.join(results_desc),
                              color=0xffc300)

        await react_message.clear_reactions()

        # Update the poll message and remove it from the JSON file
        embed.set_footer(text='Poll ID: {} (Poll ended)'.format(react_message.id))
        await react_message.edit(embed=embed)
        with open(self.polls_file, 'r') as f:
            polls = json.load(f)
        if str(react_message.id) in polls:
            del polls[str(react_message.id)]
        with open(self.polls_file, 'w') as f:
            json.dump(polls, f)


async def setup(client):
    await client.add_cog(Poll(client))
